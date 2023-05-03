from datetime import datetime

from lxml.html import HtmlElement
from requests.models import Response
from lxml import html

from app.scraper.websites.scraper import Scraper


class Immowelt(Scraper[HtmlElement]):

    def extract_title(self, entry: HtmlElement) -> str:
        return entry.xpath('.//h2/text()')[0].lower()

    def extract_list(self, response: Response) -> list[HtmlElement]:
        if response.status_code == 200:
            tree = html.fromstring(response.content)
            return tree.xpath('//div[@class=\'EstateItem-1c115\']')
        else:
            print(f"Failed to get 200 response from {self.name}, got {response.status_code}")
            return []

    def filter_on_today(self, entry: HtmlElement) -> bool:
        return True

    def filter_on_time(self, entry: HtmlElement, date_time: datetime) -> bool:
        return True

    def filter_on_special(self, entry: HtmlElement, special: set[str]) -> bool:
        item_id = self.get_id(entry)
        return item_id not in special

    def get_link(self, entry: HtmlElement) -> str:
        return entry.xpath('.//a/@href')[0]

    def is_of_special_condition(self, entry: HtmlElement) -> bool:
        return True

    def get_id(self, entry: HtmlElement) -> str:
        return entry.xpath('.//a/@id')[0]
