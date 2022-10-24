from models import Currency, Rate
from my_engine import session_scope
import PyPDF2

def get_currency():
    currencies = {}
    with session_scope() as session:
        currency = session.query(Currency).all()
        for i in currency:
            currencies[i.name] = i.id
    return (currencies)
    
def parse_pdf():
    g = []
    currencies = get_currency()        
    with open('FX_rate_Mir.pdf', 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfFileReader(pdf_file)
        for page in pdf_reader.pages: 
            for line in page.extractText().splitlines():
                b = line.split(' ')
                g.append(b)
    for a in reversed(g):
        if ":" in a[2] or ":" in a[3]:
            try:
                float(a[1].replace(',','.'))
            except ValueError:
                a[0] = a[0] + ' ' + a[1]
                a.remove(a[1])
            a[1] = float(a[1].replace(',','.'))
            a[2] = a[3] + ' ' + a[2]
            a.remove(a[3])
            a[2] = datetime.strptime(a[2], '%d.%m.%Y %H:%M')
            if a[0] in currencies:
                a[0] = currencies.get(a[0])
                # print(a)
                add = Rate(
                    currency_id = a[0],
                    value = a[1],
                    datetime = a[2]
                )
            session.add(add)