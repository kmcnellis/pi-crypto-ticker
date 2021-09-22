import pprint
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects, HTTPError
import json
import keys
import traceback

pp = pprint.PrettyPrinter(indent=4)

# ID:
# BTC: 1
# ETH: 1027
# SOL: 5426
# MOB: 7878


class Crypto(object):
    def __init__(self, *args, **kwargs):
        self.url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
        self.parameters = {
          'convert':'USD',
          # 'symbol':'BTC,ETH,SOL,MOB'
          'id':'1,1027,5426,7878'
        }
        self.headers = {
          'Accepts': 'application/json',
          'X-CMC_PRO_API_KEY': keys.coinmarketcap_key, 
        }

    def get_crypto_quotes(self):
        session = Session()
        session.headers.update(self.headers)

        try:
            response = session.get(self.url, params=self.parameters)
            response.raise_for_status()

            data = json.loads(response.text)

            watched_tickers = {"BTC":"1", "ETH":"1027", "SOL":"5426", "MOB":"7878"}
            reported_tickers = {}
            crypto_list = data["data"]

            for symbol,id in watched_tickers.items():
                crypto = crypto_list[id]
                current_price = crypto["quote"]["USD"]["price"]
                daily_volume = crypto["quote"]["USD"]["volume_24h"]
                daily_percent_change = crypto["quote"]["USD"]["percent_change_24h"]

                reported_tickers[symbol] = {}
                reported_tickers[symbol]["price"] = current_price
                reported_tickers[symbol]["volume"] = daily_volume
                reported_tickers[symbol]["change"] = daily_percent_change

            status_string = ""
            status_tuples = []
            for reported_ticker, values in reported_tickers.items():
                trend = "↓"
                trend_status = "down"
                if values["change"]>=0:
                    trend = "↑"
                    trend_status = "up"

                status_string = reported_ticker + ": " + "$" + "{:.2f}".format(values["price"]) + " "  + trend + " {:.2f}".format(values["change"]) + "%  "
                status_tuples.append((status_string, trend_status))
               #  print(status_string)
            return(status_tuples)

        except (ConnectionError, Timeout, TooManyRedirects, KeyError, HTTPError) as e:
          print("error:")
          print(e)
          print(traceback.format_exc())
          return [("error getting prices","error")]
    def getMap(self):
        url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
        parameters = {
          # 'convert':'USD'z,
          'symbol':'BTC,ETH,SOL,MOB'
          # 'id':'1,1027,5426'
        }
        session = Session()
        session.headers.update(self.headers)

        response = session.get("https://pro-api.coinmarketcap.com/v1/cryptocurrency/map", params=parameters)
        response.raise_for_status()

        data = json.loads(response.text)
        return data




if __name__ == "__main__":
    ticker = Crypto()
    pp.pprint(ticker.getMap())
    print(ticker.get_crypto_quotes())
    print(ticker.get_crypto_quotes())
