from datetime import datetime, date, timedelta
import schedule
import requests
from lxml import html
import webbrowser

URL = "https://www.ebay-kleinanzeigen.de/s-wohnung-mieten/berlin/preis::650/c203l3331+wohnung_mieten.qm_d:50,+wohnung_mieten.zimmer_d:2,+options:wohnung_mieten.built_in_kitchen_b"
payload = ""
headers = {'User-Agent': 'PostmanRuntime/7.28.2', 'Cache-Control': 'no-cache'}


def execute_data():
    print("Looking for apartment on ebay")
    with open('ebay_date_time.txt', "r") as in_file:
        for line in in_file:
            date_time_as_string = ""
            checked_highlights = list()
            if line.startswith("ebay: "):
                date_time_as_string = line.replace("ebay: ", "").replace("\n", "")
            if line.startswith("checked_highlights: "):
                checked_highlights = line.replace("checked_highlights: ", "").split(",")
            if date_time_as_string:
                prev_run_date_time = datetime.fromisoformat(date_time_as_string)
                prev_run_time = prev_run_date_time.time().replace(second=0)
                received_html = requests.request("GET", URL, headers=headers, data=payload)
                tree = html.fromstring(received_html.content)
                apt_list = tree.xpath('//article[@class=\'aditem\']')
                last_search_time = prev_run_time if prev_run_date_time.date() == date.today() \
                    else prev_run_time.replace(hour=0, minute=0)
                filtered_list = list(filter(
                    lambda x: all_filter_conditions(x, last_search_time, checked_highlights),
                    apt_list
                ))
                for apartment in filtered_list:
                    link = 'https://www.ebay-kleinanzeigen.de' + apartment.xpath('.//@data-href')[0]
                    webbrowser.open(link)
                    if has_missing_date_time(apartment):
                        checked_highlights.append(apartment.xpath('./@data-adid')[0])
                with open('ebay_date_time.txt', "w") as in_write_file:
                    updated_date_time_row = "ebay: " + datetime.now().replace(second=0).__str__()
                    updated_highlights = "checked_highlights:" + ",".join(checked_highlights)
                    ebay_line = updated_date_time_row + "\n" + updated_highlights
                    in_write_file.write(ebay_line)
            else:
                print("Couldn't find the date-time for search")


def filter_out_wbs(entry):
    title = entry.xpath('.//a[@class=\'ellipsis\']/text()')[0].lower()
    return "wbs" not in title


def filter_out_exchanges(entry):
    title = entry.xpath('.//a[@class=\'ellipsis\']/text()')[0].lower()
    return "tausch" not in title


def filter_out_limited(entry):
    title = entry.xpath('.//a[@class=\'ellipsis\']/text()')[0].lower()
    return "bis" not in title


def filter_on_today(entry):
    title = entry.xpath('.//div[@class=\'aditem-main--top--right\']/text()')[1].lower()
    return "gestern" not in title


def filter_on_time(entry, last_search_time):
    title = entry.xpath('.//div[@class=\'aditem-main--top--right\']/text()')[1].lower()
    item_publish_description = title.split(', ')
    if len(item_publish_description) > 1:
        item_publish_time_as_string = item_publish_description[1]
        item_publish_time = datetime.strptime(item_publish_time_as_string, '%H:%M').time()
        return item_publish_time > last_search_time
    return False


def filter_on_top_offers(entry, checked_highlights):
    if has_missing_date_time(entry):
        item_id = entry.xpath('./@data-adid')
        if item_id in checked_highlights:
            return False
        else:
            request_url = 'https://www.ebay-kleinanzeigen.de' + entry.xpath('.//@data-href')[0]
            response_html = requests.request("GET", request_url, headers=headers, data=payload)
            date_response = html.fromstring(response_html.content).xpath('//div[@id=\'viewad-extra-info\']/div/span/text()')[0].__str__()
            parsed_item_date = datetime.strptime(date_response, '%d.%m.%Y').date()
            return (date.today() - timedelta(days=1)) == parsed_item_date
    else:
        return True


def has_missing_date_time(entry):
    tags = entry.xpath('.//div[@class=\'aditem-main--top--right\']/i[@title=\'Top ad\' or @title=\'Highlight\']')
    return len(tags) > 0


def all_filter_conditions(entry, date_time, checked_highlights):
    return filter_out_wbs(entry) and \
           filter_out_limited(entry) and \
           filter_out_exchanges(entry) and \
           filter_on_today(entry) and \
           filter_on_top_offers(entry, checked_highlights) and \
           filter_on_time(entry, date_time)


schedule.every().minute.do(execute_data)


while 1:
    schedule.run_pending()
