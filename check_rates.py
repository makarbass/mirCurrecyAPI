import requests
from bs4 import BeautifulSoup
import hashlib
from os import path
from models import Currency, Rate
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
CHECKSUM = "checksum.txt"

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

def comp_rates():
    with session_scope() as session:
        li = dict()
        currency = session.query(Currency).all()
        for _ in currency:
            l = session.query(Currency.name, Rate.value).filter(
                Rate.currency_id == _.id).join(
                    Currency, Currency.id == Rate.currency_id).order_by(
                        Rate.id.desc()).first()
            li[l[0]] = l[1]
            if response[_.name] != li[l[0]]:
                add = Rate(
                currency_id = _.id,
                value = float(response[_.name].replace(',','.'))
                )
                session.add(add)


response = get_rates()
a = get_currency()
checksum_rates = hashlib.md5(str(response).encode("utf-8")).hexdigest()
if path.isfile(CHECKSUM):
    with open(CHECKSUM, 'r+') as file:
        checksum_file = file.readline()
        if checksum_rates != checksum_file:
            comp_rates()
        else:
            print("checksums are equals")
else:
    with open(CHECKSUM, 'w') as file:
        file.write(checksum_rates)
        comp_rates()
