from threading import Thread

from app.scraper.websites.ebay import Ebay
from app.scraper.websites.immobilienscout import Immobilienscout
from app.scraper.websites.immowelt import Immowelt
from app.scraper.websites.gewobag import Gewobag


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
        'https://www.immobilienscout24.de/Suche/de/berlin/berlin/wohnung-mieten?'
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
        'pma=700&'
        'rmi=2&'
        'sd=DESC&'
        'sf=TIMESTAMP&'
        'sp=1',
        "GET",
        {'User-Agent': 'PostmanRuntime/7.28.2', 'Cache-Control': 'no-cache'}
    )
    gewobag = Gewobag(
        "gewobag",
        'https://www.gewobag.de/fuer-mieter-und-mietinteressenten/mietangebote/?bezirke_all=&bezirke%5B%5D=charlottenburg-wilmersdorf&bezirke%5B%5D=charlottenburg-wilmersdorf-charlottenburg&bezirke%5B%5D=charlottenburg-wilmersdorf-nord&bezirke%5B%5D=charlottenburg-wilmersdorf-grunewald&bezirke%5B%5D=charlottenburg-wilmersdorf-wilmersdorf&bezirke%5B%5D=friedrichshain-kreuzberg&bezirke%5B%5D=friedrichshain-kreuzberg-friedrichshain&bezirke%5B%5D=friedrichshain-kreuzberg-kreuzberg&bezirke%5B%5D=lichtenberg&bezirke%5B%5D=lichtenberg-alt-hohenschoenhausen&bezirke%5B%5D=lichtenberg-falkenberg&bezirke%5B%5D=lichtenberg-fennpfuhl&bezirke%5B%5D=lichtenberg-friedrichsfelde&bezirke%5B%5D=marzahn-hellersdorf&bezirke%5B%5D=marzahn-hellersdorf-marzahn&bezirke%5B%5D=mitte&bezirke%5B%5D=mitte-tiergarten&bezirke%5B%5D=neukoelln&bezirke%5B%5D=neukoelln-britz&bezirke%5B%5D=neukoelln-buckow&bezirke%5B%5D=pankow&bezirke%5B%5D=pankow-prenzlauer-berg&bezirke%5B%5D=reinickendorf&bezirke%5B%5D=reinickendorf-hermsdorf&bezirke%5B%5D=reinickendorf-tegel&bezirke%5B%5D=reinickendorf-waidmannslust&bezirke%5B%5D=spandau&bezirke%5B%5D=spandau-haselhorst&bezirke%5B%5D=spandau-staaken&bezirke%5B%5D=spandau-wilhelmstadt&bezirke%5B%5D=steglitz-zehlendorf&bezirke%5B%5D=steglitz-zehlendorf-lichterfelde&bezirke%5B%5D=steglitz-zehlendorf-wannsee&bezirke%5B%5D=steglitz-zehlendorf-zehlendorf&bezirke%5B%5D=tempelhof-schoeneberg&bezirke%5B%5D=tempelhof-schoeneberg-mariendorf&bezirke%5B%5D=tempelhof-schoeneberg-schoeneberg&bezirke%5B%5D=treptow-koepenick&bezirke%5B%5D=treptow-koepenick-alt-treptow&nutzungsarten%5B%5D=wohnung&sort-by=recent',
        'GET',
        {'User-Agent': 'PostmanRuntime/7.28.2', 'Cache-Control': 'no-cache'}
    )
    Thread(target=ebay.start).start()
    #Thread(target=immoscout.start).start() Needs to update a link and maybe the parser as well
    Thread(target=immowelt.start).start()
    Thread(target=gewobag.start).start()


main()
