from datetime import datetime

from lxml.html import HtmlElement
from requests.models import Response
from lxml import html

from app.scraper.websites.scraper import Scraper


class Immowelt(Scraper[HtmlElement]):

    def extract_list(self, response: Response) -> list[HtmlElement]:
        tree = html.fromstring(response.content)
        return tree.xpath('//div[@class=\'EstateItem-1c115\']')

    def filter_out_wbs(self, entry: HtmlElement) -> bool:
        title = entry.xpath('.//h2/text()')[0].lower()
        return "wbs" not in title

    def filter_out_exchanges(self, entry: HtmlElement) -> bool:
        title = entry.xpath('.//h2/text()')[0].lower()
        return "tausch" not in title

    def filter_out_limited(self, entry: HtmlElement) -> bool:
        title = entry.xpath('.//h2/text()')[0].lower()
        return "bis" not in title

    def filter_on_today(self, entry: HtmlElement) -> bool:
        return True

    def filter_on_time(self, entry: HtmlElement, date_time: datetime) -> bool:
        return True

    def filter_on_special(self, entry: HtmlElement, special: set[str]) -> bool:
        item_id = self.get_id(entry)
        return item_id not in special

    def filter_out_sublease(self, entry: HtmlElement) -> bool:
        title = entry.xpath('.//h2/text()')[0].lower()
        return "untermiete" not in title

    def get_link(self, entry: HtmlElement) -> str:
        return entry.xpath('.//a/@href')[0]

    def is_of_special_condition(self, entry: HtmlElement) -> bool:
        return True

    def get_id(self, entry: HtmlElement) -> str:
        return entry.xpath('.//a/@id')[0]
