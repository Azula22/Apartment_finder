from datetime import datetime, date
from typing import Any

import requests
from lxml import html
from lxml.html import HtmlElement
from requests.models import Response

from app.scraper.websites.scraper import Scraper


def has_missing_date_time(entry: HtmlElement):
    tags = entry.xpath('.//div[@class=\'aditem-main--top--right\']/i[@title=\'Top ad\' or @title=\'Highlight\']')
    return len(tags) > 0


class Ebay(Scraper[HtmlElement]):

    def is_of_special_condition(self, entry: HtmlElement) -> bool:
        tags = entry.xpath('.//div[@class=\'aditem-main--top--right\']/i[@title=\'Top ad\' or @title=\'Highlight\']')
        return len(tags) > 0

    def get_id(self, entry: HtmlElement) -> str:
        return entry.xpath('./@data-adid')[0]

    def extract_list(self, response: Response) -> list[HtmlElement]:
        tree = html.fromstring(response.content)
        return tree.xpath('//article[@class=\'aditem\']')

    def get_link(self, entry: HtmlElement) -> Any:
        return f"https://www.ebay-kleinanzeigen.de{entry.xpath('.//@data-href')[0]}"

    def filter_out_wbs(self, entry: HtmlElement):
        title = entry.xpath('.//a[@class=\'ellipsis\']/text()')[0].lower()
        return "wbs" not in title

    def filter_out_sublease(self, entry: HtmlElement) -> bool:
        title = entry.xpath('.//a[@class=\'ellipsis\']/text()')[0].lower()
        return "untermiete" not in title

    def filter_out_exchanges(self, entry: HtmlElement):
        title = entry.xpath('.//a[@class=\'ellipsis\']/text()')[0].lower()
        return "tausch" not in title

    def filter_out_limited(self, entry: HtmlElement):
        title = entry.xpath('.//a[@class=\'ellipsis\']/text()')[0].lower()
        return "bis" not in title

    def filter_on_today(self, entry: HtmlElement):
        title = entry.xpath('.//div[@class=\'aditem-main--top--right\']/text()')[1].lower()
        return "gestern" not in title

    def filter_on_time(self, entry: HtmlElement, date_time: datetime):
        title = entry.xpath('.//div[@class=\'aditem-main--top--right\']/text()')[1].lower()
        item_publish_description = title.split(', ')
        if len(item_publish_description) > 1:
            item_publish_time_as_string = item_publish_description[1]
            item_publish_time = datetime.strptime(item_publish_time_as_string, '%H:%M').time()
            return item_publish_time > date_time.time()
        return False

    def filter_on_special(self, entry: HtmlElement, special: set[str]):
        if has_missing_date_time(entry):
            item_id = entry.xpath('./@data-adid')[0]
            if item_id in special:
                return False
            else:
                request_url = 'https://www.ebay-kleinanzeigen.de' + entry.xpath('.//@data-href')[0]
                response_html = requests.request("GET", request_url, headers=self.headers)
                date_response_as_list = html \
                    .fromstring(response_html.content) \
                    .xpath('//div[@id=\'viewad-extra-info\']/div/span/text()')
                if date_response_as_list:
                    date_response = date_response_as_list[0].__str__()
                    parsed_item_date = datetime.strptime(date_response, '%d.%m.%Y').date()
                    return date.today() == parsed_item_date
        else:
            return True
