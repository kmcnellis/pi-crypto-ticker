# pi-crypto-ticker
RGB LED Display of Cryto Prices, weather, and time.

## Getting started
This code assumes two 32x64 RGB matrixes, wired in serial, with a Rasberry Pi and a [Adafruit RGB Matrix Bonnet](https://learn.adafruit.com/adafruit-rgb-matrix-bonnet-for-raspberry-pi) driving them.

Follow [this guide](https://learn.adafruit.com/adafruit-rgb-matrix-bonnet-for-raspberry-pi/driving-matrices) to get setup & wire your Pi & Matrix.

You'll also need to ensure that Python3 is installed.  [PM2](https://pm2.keymetrics.io/docs/usage/quick-start/) is also used for running on startup.

First, to install python and other dependancies
```sh
sudo apt-get install python3 python3-dev cython3 python3-pillow libgraphicsmagick++-dev libwebp-dev
```

Then to setup the bonnet:
```sh
git clone git@github.com:hzeller/rpi-rgb-led-matrix.git
curl https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/master/rgb-matrix.sh >rgb-matrix.sh
chmod +x rgb-matrix.sh
sudo bash rgb-matrix.sh
```


## Running the Code
1. Log into your Pi and follow the Getting started steps.
2. Downlaod the code to the Pi
   ```sh
   git clone git@github.com:kmcnellis/pisign.git
   ```
3. Copy keys.sample.py to keys.py and add your API keys
4. Add your latitude and longitude to weather.py
5. Create a python Virtual Env
   ```sh
   python -m venv .venv
   ```
6. Activate the venv
   ```sh
   source .venv/bin/activate
   ```
7. Install dependancies
   ```sh
   source Source/.venv/bin/activate
   .venv/bin/pip install -r requirements.txt
   ```
8. Run
   ```sh
   sudo python3 main.py
   ```

### PM2 Setup
1. Install
   ```sh
   sudo apt-get install npm
   npm install pm2 -g
   ```
2. Setup Daemon (run the printed commands)
   ```sh
   pm2 startup #Follow the commands printed
   ```
3. Edit `start.sh` to include the correct (absolute) path to your main.py and .venv
4. Run the start script
   ```sh
   ./start.sh
   ```
