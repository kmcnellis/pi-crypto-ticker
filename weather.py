from pyowm import OWM
from pyowm.utils import config
from pyowm.utils import timestamps
import pprint
from PIL import Image
from io import BytesIO
import requests
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects, HTTPError
import keys
import os
from pyowm.utils.config import get_default_config_for_subscription_type
from pyowm.utils.config import get_default_config_for_proxy

location = {"latitude":30.2572506, "longitude":-97.760047} # Austin,TX
script_dir = os.path.dirname(__file__)

class Weather(object):
    def __init__(self, *args, **kwargs):
        config_dict = get_default_config_for_subscription_type('free')
        owm = OWM(keys.owm_key,config_dict)
        self.mgr = owm.weather_manager()
        self.mgr.http_client.http = requests
        # Pip isn't yet updated (https://github.com/csparpa/pyowm/blob/master/pyowm/weatherapi30/uris.py#L5)
        self.mgr.http_client.root_uri = "openweathermap.org/data/3.0"
        self.icons = {}
        self.image_url =  "http://openweathermap.org/img/wn/"

    def get(self):
        one_call = self.mgr.one_call(lat=location["latitude"], lon=location["longitude"], exclude='minutely,hourly,alerts', units='imperial')
        print(one_call)
        current = one_call.current
        current_temp = current.temperature()
        forcast = one_call.forecast_daily[0]
        forcast_temp = forcast.temperature()
        print("precipitation_probability",forcast.precipitation_probability)
        print("rain",forcast.rain)
        print("snow",forcast.snow)

        current_icon_name = current.weather_icon_name
        current_icon = self.getIcon(current_icon_name)

        forcast_icon_name = forcast.weather_icon_name
        forcast_icon = self.getIcon(forcast_icon_name)

        # https://github.com/csparpa/pyowm/blob/0474b61cc67fa3c95f9e572b96d3248031828fce/pyowm/weatherapi25/weather.py#L11
        return {
            'current': {
                'icon': current_icon,
                'temp': current_temp.get('temp'),
                'status': current.status,
                'detail': current.detailed_status,
                'humidity':current.humidity,
            },
            'forcast': {
                'icon': forcast_icon,
                'high':forcast_temp.get('max', None),
                'low':forcast_temp.get('min', None),
                'day':forcast_temp.get('day', None),
                'night':forcast_temp.get('night', None),
                'humidity':forcast.humidity,
                'precipitation_probability':forcast.precipitation_probability,
                'status':forcast.status,
                'detail':forcast.detailed_status,
            }
        }
    def getIcon(self, icon_name):
        path = f'icons/{icon_name}.png'
        path = os.path.join(script_dir, path)
        return Image.open(path).convert('RGB')
        # if icon_name in self.icons:
        #     icon = self.icons[icon_name]
        #     return icon
        # else:
        #     try:
        #         response = requests.get(self.image_url+icon_name+"@2x.png")
        #         img = Image.open(BytesIO(response.content))
        #         icon = img.convert('RGB')
        #         self.icons[icon_name] = icon
        #         return icon
        #     except (ConnectionError, Timeout, TooManyRedirects, KeyError, HTTPError) as e:
        #         print("error:")
        #         print(e)
        #         print(traceback.format_exc())
        #         return None



# Search for current weather in London (Great Britain) and get details
"""
w = observation.weather

w.detailed_status         # 'clouds'
w.wind()                  # {'speed': 4.6, 'deg': 330}
w.humidity                # 87
w.temperature('celsius')  # {'temp_max': 10.5, 'temp': 9.7, 'temp_min': 9.0}
w.rain                    # {}
w.heat_index              # None
w.clouds                  # 75

# Will it be clear tomorrow at this time in Milan (Italy) ?
forecast = mgr.forecast_at_place('Milan,IT', 'daily')
answer = forecast.will_be_clear_at(timestamps.tomorrow())
"""
# austin: 30.2572506,-97.760047

if __name__ == "__main__":
    pp = pprint.PrettyPrinter(indent=4)
    w = Weather()
    pp.pprint(w.get())
