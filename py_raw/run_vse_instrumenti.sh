#!/usr/bin/env fish
export DISPLAY=:0
export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
date > /home/krot/5/competitor_prices/logs/process.log
python3 /home/krot/5/competitor_prices/py_raw/vse_instrumenti_parser.py 1>1 2>>/home/krot/5/competitor_prices/logs/process.log
date >> /home/krot/5/competitor_prices/logs/process.log

