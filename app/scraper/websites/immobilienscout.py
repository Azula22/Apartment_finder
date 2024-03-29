from typing import Any

from lxml.html import HtmlElement
from requests.models import Response

from app.scraper.websites.scraper import Scraper, T
from datetime import datetime


class Immobilienscout(Scraper[dict]):

    def extract_title(self, entry: HtmlElement) -> str:
        return entry["resultlist.realEstate"]["title"].lower()

    def is_of_special_condition(self, entry: T) -> bool:
        return False

    def get_id(self, entry: dict) -> str:
        return entry["realEstateId"]

    def extract_list(self, response: Response) -> list[dict]:
        return response.json()["searchResponseModel"]["resultlist.resultlist"]["resultlistEntries"][0]["resultlistEntry"]

    def get_link(self, entry: dict) -> Any:
        entry_id = entry["realEstateId"]
        return f"https://www.immobilienscout24.de/expose/{entry_id}/#/"

    def filter_on_today(self, entry: dict):
        return True

    def filter_on_time(self, entry: dict, date_time: datetime):
        entry_date_time = datetime.fromisoformat(entry["@publishDate"])
        return entry_date_time >= date_time.astimezone(entry_date_time.tzinfo)

    def filter_on_special(self, entry: dict, special: set[str]):
        return True
