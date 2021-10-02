import json
import requests
from config import keys, YOUR_ACCESS_KEY


class APIException(Exception):
    pass


class ExchangeRates:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        if quote == base:
            raise APIException(f'Невозможно перевести одинаковые валюты {base}.')

        try:
            quote_tiker = keys[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {quote}')

        try:
            base_tiker = keys[base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать кол-во {amount}')

        r = requests.get(f'http://api.exchangeratesapi.io/v1/latest?access_key={YOUR_ACCESS_KEY}'
                         f'&base=EUR&symbols={quote_tiker},{base_tiker}')
        total_temp = json.loads(r.content)['rates']  # ответ в формате {'USD': 1.159549, 'RUB': 84.267461}
        total_base = round(((total_temp[base_tiker] / total_temp[quote_tiker]) * amount), 4)
        return total_base
