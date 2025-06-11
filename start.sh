pm2 start /home/pi/Source/pisign/main.py --interpreter=/home/pi/Source/.venv/bin/python3 --name=ticker  --kill-timeout 3000
pm2 save
