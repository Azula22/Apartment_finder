import webbrowser
from abc import ABC, abstractmethod
from datetime import datetime, date
from time import sleep
from typing import Optional
from typing import TypeVar, Generic

import requests
from requests import Response

from app.scraper.models.FileBody import FileBody

T = TypeVar('T')


class Scraper(ABC, Generic[T]):

    def __init__(self, name: str, url: str, method: str, headers: object) -> None:
        self.url = url
        self.name = name
        self.headers = headers
        self.method = method

    def start(self) -> None:
        print(f"{datetime.now().__str__()} Looking for apt {self.name}")
        file_body = self.get_file_body()
        special_cases = file_body.checked
        response = requests.request(self.method, self.url, headers=self.headers)
        apartment_list = self.extract_list(response)
        search_date_time = file_body.date_time.replace(second=0) if file_body.date_time.date() == date.today() \
            else file_body.date_time.replace(hour=0, second=0, minute=0)
        filtered_apartments = list(filter(
            lambda e: self.all_filter_conditions(e, search_date_time, file_body.checked),
            apartment_list
        ))
        for apartment in filtered_apartments:
            link = self.get_link(apartment)
            webbrowser.open(link)
            print(f"Apartment found {link}")
            if self.is_of_special_condition(apartment):
                special_cases.add(self.get_id(apartment))
        self.write_file_body(FileBody(datetime.now().replace(second=0), special_cases))
        sleep(60)
        self.start()

    def get_file_body(self) -> Optional[FileBody]:
        date_time = None
        checked_highlights = list()
        today = datetime.today().day
        with open(f"./files/{self.name}.txt", "r") as in_file:
            for line in in_file:
                if line.startswith(self.name + ": "):
                    date_time_as_string = line.replace(self.name + ": ", "").replace("\n", "")
                    date_time = datetime.fromisoformat(date_time_as_string)
                if line.startswith("checked_highlights: "):
                    checked_highlights = set(line.replace("checked_highlights: ", "").replace("\n", "").split(","))
            if date_time is None:
                print("Couldn't find date_time info")
            if date_time is not None and date_time.day != today:
                date_time = date_time.replace(day=today, hour=0, minute=0, second=0, microsecond=0)
                checked_highlights = list()
        return None if date_time is None else FileBody(date_time, checked_highlights)

    def write_file_body(self, file_body: FileBody) -> None:
        lines = list()
        with open(f"./files/{self.name}.txt", "w") as in_file:
            lines.append(f"{self.name}: {file_body.date_time.__str__()}")
            lines.append(f"checked_highlights: {','.join(file_body.checked)}")
            in_file.write("\n".join(lines))

    def all_filter_conditions(self, entry: T, date_time: datetime, checked_highlights: set[str]) -> bool:
        return self.filter_out_wbs(entry) and \
               self.filter_out_limited(entry) and \
               self.filter_out_exchanges(entry) and \
               self.filter_on_today(entry) and \
               self.filter_on_special(entry, checked_highlights) and \
               self.filter_on_time(entry, date_time) and \
               self.filter_out_sublease(entry)

    @abstractmethod
    def extract_list(self, response: Response) -> list[T]:
        pass

    @abstractmethod
    def filter_out_wbs(self, entry: T) -> bool:
        pass

    @abstractmethod
    def filter_out_exchanges(self, entry: T) -> bool:
        pass

    @abstractmethod
    def filter_out_limited(self, entry: T) -> bool:
        pass

    @abstractmethod
    def filter_on_today(self, entry: T) -> bool:
        pass

    @abstractmethod
    def filter_on_time(self, entry: T, date_time: datetime) -> bool:
        pass

    @abstractmethod
    def filter_on_special(self, entry: T, special: set[str]) -> bool:
        pass

    @abstractmethod
    def filter_out_sublease(self, entry: T) -> bool:
        pass

    @abstractmethod
    def get_link(self, entry: T) -> str:
        pass

    @abstractmethod
    def is_of_special_condition(self, entry: T) -> bool:
        pass

    @abstractmethod
    def get_id(self, entry: T) -> str:
        pass
