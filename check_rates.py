import requests
from bs4 import BeautifulSoup
import hashlib
from models import Currency, Rate, Hashsum
from my_engine import session_scope
from functions import get_currency

LINK = "https://mironline.ru/support/list/kursy_mir/"
HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)  Safari/537.36',
    'Referer': 'https://mironline.ru/support/list/',
    'Connection': 'keep-alive',
}

def get_rates() -> dict:
    client = requests.session()
    html = client.get(LINK, headers= HEADERS)
    table = BeautifulSoup(html.text, 'lxml').find(
        'table').find_all(
            'td')
    contents = []
    for row in table:
        contents.append(
            row.p.text.replace(
                '\r\n\t\t\t','').replace(
                    '\r\n\t\t','').strip())
    cell = dict(zip(contents[::2], contents[1::2]))
    return cell


def comp_rates(response):
    li = []
    for _ in response.keys():
        l = session.query(Currency.name, Rate.value, Currency.id).filter(Currency.name == _).join(
                Currency, Currency.id == Rate.currency_id).order_by(
                    Rate.id.desc()).first()
        if response[_] != l[1]:
            li.append(Rate(
                currency_id = l.id,
                value = float(response[_].replace(',','.'))
            ))
    session.add_all(li)


response = get_rates()
a = get_currency()
checksum_rates = hashlib.md5(str(response).encode("utf-8")).hexdigest()
with session_scope() as session:
    put = Hashsum(hashsum = checksum_rates)
    checksum_db = session.query(Hashsum.hashsum).one_or_none()
    if checksum_db:
        if checksum_rates != checksum_db[0]:
            comp_rates(response)
            session.query(Hashsum).filter(
                Hashsum.hashsum == checksum_db[0]
                ).update(
                    {
                        "hashsum": checksum_rates
                        }, synchronize_session="fetch")     
        else:
            print("checksums are equals")
    else:
            comp_rates(response)
            session.add(put)