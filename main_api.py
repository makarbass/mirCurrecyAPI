from datetime import datetime, timedelta
from models import Currency, Rate
from my_engine import session_scope
from config import API
from flask import Flask, Response, json
from flask_restful import Api, Resource, reqparse
from flask.wrappers import Request
from functions import get_currency
                        
class AnyJsonRequest(Request):
    def on_json_loading_failed(self, e):
        if e is not None:
            return super().on_json_loading_failed(e)

app = Flask(__name__)
api = Api(app, prefix='')
app.request_class = AnyJsonRequest

class _Resource(Resource):
    parser = reqparse.RequestParser(trim=True)
    #parser.add_argument('parser', type=str, default=False, required=True, choices=('M', 'F'), help='Bad choice: {error_msg}')

    def return_json(self, body, status):
        return Response(json.dumps(body, ensure_ascii=False), mimetype='application/json', status=status)

    def return_status(self, status):
        return Response(status=status)


class GetRate(_Resource):
    parser = reqparse.RequestParser(trim=True)
    parser.add_argument('currency', type=int)
    parser.add_argument('beginDate', type = str)
    parser.add_argument('endDate', type = str)

    def get(self):
        args = self.parser.parse_args()
        li = []
        beginDate = args['beginDate']
        endDate = args['endDate']
        if args['currency'] is None:
            with session_scope() as session:
                currency = session.query(Currency).all()
                for _ in currency:
                    l = session.query(Rate.currency_id, Rate.value, Currency.name, Currency.ticker).join(
                        Currency, Currency.id == Rate.currency_id).filter(
                        Currency.id == _.id).order_by(
                            Rate.id.desc()).first()
                    li.append({
                        'currency': l[0],
                        'value': l[1],
                        'name':l[2],
                        'ticker':l[3]
                    })
                return {"rate": li}
        if endDate is None:
            endDate = datetime.today() 
        else:
            endDate = datetime.strptime(endDate, '%Y-%m-%d')
        endDate = endDate.replace(hour=23, minute=59, second = 59, microsecond = 999999)
        if beginDate is None:
            beginDate = datetime.combine(endDate - timedelta(days=7) , datetime.min.time())
        with session_scope() as session:
            cur = session.query(Currency.id).filter(
                Currency.id == args['currency']).one_or_none()
            if cur is not None:
                sel = session.query(Rate.datetime, Rate.value, Currency.name, Currency.ticker).filter(
                    Rate.currency_id == args['currency']
                    ).filter(
                        Rate.datetime <= endDate
                        ).filter(
                            Rate.datetime >=beginDate
                            ).join(
                                Currency, Currency.id == Rate.currency_id
                                ).all()
                try:
                    ticker = sel[0].ticker
                except:
                    ticker = None
                try:
                    name = sel[0].name
                except:
                    name = None
                for _ in sel:
                    li.append({
                        'date': str(_.datetime),
                        'rate': _.value})
                return {"beginDate": f'{beginDate}', "endDate": f'{endDate}',
                "name": f'{name}', "ticker": f'{ticker}', 
                "values": li}
            else:
                return {"status": 404, "message": "Currency not found"}


api.add_resource(GetRate, '/rate')

if __name__ == '__main__':
    app.run(host=API.get('host'), port=API.getint(
        'port'), debug=API.getboolean('debug'))
