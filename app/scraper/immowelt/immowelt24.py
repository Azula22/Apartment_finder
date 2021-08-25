import requests
from datetime import datetime, timedelta, timezone
import schedule
import webbrowser

URL = 'https://www.immobilienscout24.de/Suche/de/berlin/berlin/wohnung-mit-einbaukueche-mieten?' \
      'numberofrooms=2.0-&' \
      'price=-800.0&' \
      'livingspace=52.0-&' \
      'pricetype=calculatedtotalrent' \
      '&sorting=2' \
      '&enteredFrom=result_list'

def execute_data():
    print("Looking for apartment on immowelt")
    date_time_line = ""
    with open('immowelt_date_time.txt', "r") as in_file:
        for line in in_file:
            if line.startswith("immowelt: "):
                date_time_as_string = line.replace("immowelt: ", "")
                date_time = datetime.fromisoformat(date_time_as_string)
                immo_page = requests.post(URL).json()["searchResponseModel"]["resultlist.resultlist"]["resultlistEntries"][0]["resultlistEntry"]
                valid_apartments = list(filter(lambda e: all_filter_conditions(e, date_time), immo_page))
                apartment_ids = list(map(get_id, valid_apartments))
                for apartment_id in apartment_ids:
                    webbrowser.open(f"https://www.immobilienscout24.de/expose/{apartment_id}/")
                new_date_time = datetime.now(timezone.utc) - timedelta(seconds=2)
                date_time_line = line.replace(date_time_as_string, new_date_time.isoformat())
                with open('immowelt_date_time.txt', "w") as in_write_file:
                    in_write_file.write(date_time_line)


def filter_out_wbs(entry):
    title = entry["resultlist.realEstate"]["title"].lower()
    return "wbs" not in title


def filter_out_exchanges(entry):
    title = entry["resultlist.realEstate"]["title"].lower()
    return "tauschwohnung" not in title


def filter_out_private(entry):
    is_private = entry["resultlist.realEstate"]["privateOffer"].lower() == "true"
    return not is_private


def filter_out_checked_apartments(entry, date_time):
    return datetime.fromisoformat(entry["@publishDate"]) >= date_time


def get_id(entry):
    return entry["realEstateId"]


def get_publish_date(entry):
    return entry["@publishDate"]


def all_filter_conditions(entry, date_time):
    return filter_out_wbs(entry) and \
           filter_out_exchanges(entry) and \
           filter_out_private(entry) and \
           filter_out_checked_apartments(entry, date_time)


schedule.every().minute.do(execute_data)


while 1:
    schedule.run_pending()