import requests
from matrix import MatrixBase
from ticker import Crypto
from weather import Weather
from rgbmatrix import graphics
import time
from PIL import Image
import threading
from datetime import datetime
from datetime import timedelta
import traceback
from math import floor


black = graphics.Color(0, 0, 0)
white = graphics.Color(255, 255, 255)
darkRed = graphics.Color(102, 0, 0)
grey = graphics.Color(96, 96, 96)
lightBlue = graphics.Color(108, 119, 122)
darkGrey = graphics.Color(30, 30, 30)
red = graphics.Color(255, 0, 0)
green = graphics.Color(0, 255, 0)
blue = graphics.Color(0, 0, 255)
font = graphics.Font()
font.LoadFont("/home/pi/rpi-rgb-led-matrix/fonts/9x18.bdf")

statusFont = graphics.Font()
statusFont.LoadFont("/home/pi/rpi-rgb-led-matrix/fonts/5x8.bdf")

textColor = white
dateformat= "%m/%d %H:%M"
timeformat= "%H:%M"

class RunText(MatrixBase):
    def __init__(self, *args, **kwargs):
        super(RunText, self).__init__(*args, **kwargs)
        self.parser.add_argument("-i", "--image", help="The image to display", default="/home/pi/rpi-rgb-led-matrix/examples-api-use/runtext.ppm")
        self.lock = threading.Lock()
        self.prices = [("loading....","status")]
        self.forcast = None
        self.updatedAt = None
        download_thread = threading.Thread(target=self.getCrypto, name="getCrypto")
        download_thread.daemon=True
        download_thread.start()

        status_thread = threading.Thread(target=self.getWeather, name="getStatus")
        status_thread.daemon=True
        status_thread.start()

    def getWeather(self):
        w = Weather()
        while True:
            print("loading weather...")
            try:
                forcast = w.get()
                self.lock.acquire()
                self.forcast = forcast
                self.lock.release()
                print("forcast:")
                print(forcast)
            except Exception as e:
                    print("error:")
                    print(e)
                    print(traceback.format_exc())
                    self.lock.acquire()
                    self.forcast = None
                    self.lock.release()
            time.sleep(60*5) # 5 minutes



    def getCrypto(self):
        ticker = Crypto()
        errors = 0
        while True:
            print("loading crypto prices...")
            try:
                prices = ticker.get_crypto_quotes()
                self.lock.acquire()
                self.prices = prices
                self.updatedAt = datetime.now()
                self.lock.release()
                print("prices:")
                print(self.updatedAt)
                print(prices)
                errors = 0
            except Exception as e:
                    errors +=1
                    print("error:")
                    print(e)
                    print(traceback.format_exc())
                    if errors > 1:
                        self.lock.acquire()
                        self.prices = [("error getting prices","error")]
                        self.lock.release()
            time.sleep(60*5.0001)


    def run(self):
        if not 'image' in self.__dict__:
            self.image = Image.open(self.args.image).convert('RGB')
        self.image.resize((self.matrix.width, self.matrix.height), Image.ANTIALIAS)
        self.canvas = self.matrix.CreateFrameCanvas()

        self.pos = self.canvas.width

        while True:
            self.pos -= 1
            self.draw()
            time.sleep(0.015)
            self.canvas = self.matrix.SwapOnVSync(self.canvas)

    def draw(self):
        self.canvas.Clear()
        self.lock.acquire()
        prices = self.prices
        updatedAt = self.updatedAt
        self.lock.release()
        position = self.pos

        for t in prices:
            s = t[0]
            color = lightBlue
            if t[1] == "up":
                color = green
            if t[1] == "down":
                color = red
            if t[1] == "error":
                color = darkRed
            length = graphics.DrawText(self.canvas, font, position, self.matrix.height-2, color, s)
            position += length+3

        if (position < 10):
            self.pos = self.canvas.width

        if self.forcast != None:
            temp = self.forcast['current']['temp']
            temp_f = "{:.1f}".format(temp)
            humidity = self.forcast['current']['humidity']
            if humidity >=35:
                weather = f'{temp_f}° {humidity}%'
            else:
                weather = f'{temp_f}°'

            color = lightBlue
            if temp > 85:
                color = red
            elif temp < 65:
                color = blue

            high=self.forcast['forcast']['high']
            high_f = "{:.1f}".format(high)
            f_humidity = self.forcast['forcast']['humidity']
            if f_humidity >=30:
                forcast = f'{high_f}° {f_humidity}%'
            else:
                forcast = f'{high_f}°'

            graphics.DrawText(self.canvas, statusFont, 17,  8, color, weather)
            graphics.DrawText(self.canvas, statusFont, 17,  16, darkGrey, forcast)
            self.canvas.SetImage(self.forcast['current']['icon'], 0, 0, unsafe=False)
            # self.canvas.SetImage(self.image, -self.pos)

        # graphics.DrawLine(self.canvas, 0, 15, self.matrix.width, 15, darkGrey)
        now = datetime.now()
        dt_string = now.strftime(dateformat)
        graphics.DrawText(self.canvas, statusFont, self.matrix.width-len(dt_string*5)-1, 8, lightBlue, dt_string)

        updated = ""
        if self.updatedAt != None:
            difference = floor((now - updatedAt).total_seconds() / 60)
            updated = f'-{difference}m '
            color = lightBlue
            if difference > 10:
                color = red
            elif difference > 5:
                color = darkRed
            elif difference > 0:
                color = darkGrey

            if difference > 0:
                graphics.DrawText(self.canvas, statusFont, self.matrix.width-len(updated*5)-1, 16, color, updated)
        elif len(prices)>1:
            updated = f'out of date'
            graphics.DrawText(self.canvas, statusFont, self.matrix.width-len(updated*5)-1, 16, darkRed, updated)


if __name__ == "__main__":
    run_text = RunText()
    if (not run_text.process()):
        run_text.print_help()


    r = requests.get("https://api.coinmarketcap.com/v1/ticker/")
    data = r.json()
    print(data)
    # x = PrettyTable()
    # x.field_names = [ "Crypto Name", "Symbol", "Price in USD"]
    #
    # for crypto in data:
    #     x.add_row([ crypto['name'], crypto['symbol'], crypto['price_usd'] ])
    #
    # print(x)
