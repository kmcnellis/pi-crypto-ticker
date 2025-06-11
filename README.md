# pi-crypto-ticker
RGB LED Display of Cryto Prices, weather, and time.

## Getting started
This code assumes two 32x64 RGB matrixes, wired in serial, with a Rasberry Pi and a [Adafruit RGB Matrix Bonnet](https://learn.adafruit.com/adafruit-rgb-matrix-bonnet-for-raspberry-pi) driving them.

Follow [this guide](https://learn.adafruit.com/adafruit-rgb-matrix-bonnet-for-raspberry-pi/driving-matrices) to get setup & wire your Pi & Matrix.

Specifically, run:

```sh
curl https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/master/rgb-matrix.sh >rgb-matrix.sh
sudo bash rgb-matrix.sh
```

You'll also need to ensure that Python3 is installed.

## Running the Code
1. Log into your Pi and follow the Getting started steps.
2. Downlaod the code to the Pi
3. Copy keys.sample.py to keys.py and add your API keys
4. Add your latitude and longitude to weather.py
5. Run
```sh
source bin/activate
```
6. Run
```sh
sudo python3 main.py
```
