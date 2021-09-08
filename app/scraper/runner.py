from threading import Thread

from app.scraper.ebay import Ebay
from app.scraper.immobilienscout import Immobilienscout
from app.scraper.immowelt import Immowelt


def main():
    ebay = Ebay(
        "ebay",
        "https://www.ebay-kleinanzeigen.de/s-wohnung-mieten/berlin/"
        "preis::650/"
        "c203l3331+wohnung_mieten.qm_d:50,"
        "+wohnung_mieten.zimmer_d:2,"
        "+options:wohnung_mieten.built_in_kitchen_b",
        "GET",
        {'User-Agent': 'PostmanRuntime/7.28.2', 'Cache-Control': 'no-cache'}
    )
    immoscout = Immobilienscout(
        "immobilienscout",
        'https://www.immobilienscout24.de/Suche/de/berlin/berlin/wohnung-mit-einbaukueche-mieten?'
        'numberofrooms=2.0-&'
        'price=-850.0&'
        'livingspace=52.0-&'
        'pricetype=calculatedtotalrent'
        '&sorting=2'
        '&enteredFrom=result_list',
        "POST",
        {'Cache-Control': 'no-cache'}
    )
    immowelt = Immowelt(
        "immowelt",
        'https://www.immowelt.de/liste/berlin/wohnungen/mieten?'
        'ami=50&'
        'd=true&'
        'ffs=FITTED_KITCHEN&'
        'pma=700&'
        'rmi=2&'
        'sd=DESC&'
        'sf=TIMESTAMP&'
        'sp=1',
        "GET",
        {'User-Agent': 'PostmanRuntime/7.28.2', 'Cache-Control': 'no-cache'}
    )
    Thread(target=ebay.start).start()
    Thread(target=immoscout.start).start()
    Thread(target=immowelt.start).start()


main()
