from datetime import datetime

from lxml import html
from lxml.html import HtmlElement
from requests.models import Response

from app.scraper.websites.scraper import Scraper, T


class Gewobag(Scraper[dict]):

    def extract_title(self, entry: HtmlElement) -> str:
        return entry.xpath('.//article/div/a[@class=\'angebot-header\']/address/text()')[0].lower()

    def extract_list(self, response: Response) -> list[T]:
        tree = html.fromstring(response.content)
        return tree.xpath('//div[@class=\'filtered-elements\']')

    def filter_on_today(self, entry: T) -> bool:
        return True

    def filter_on_time(self, entry: T, date_time: datetime) -> bool:
        return True

    def filter_on_special(self, entry: T, special: set[str]) -> bool:
        item_id = self.get_id(entry)
        return item_id not in special

    def get_link(self, entry: T) -> str:
        return entry.xpath('.//article/div/a[@class=\'angebot-header\']/@href')[0]

    def is_of_special_condition(self, entry: T) -> bool:
        return True

    def get_id(self, entry: T) -> str:
        return entry.xpath('.//article/@id')[0]
