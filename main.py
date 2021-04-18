from bot import Bot
from assets.credentials import *
import signal
import sys
import time




trader = Bot(BINANCE_KEY, BIANCE_SECRET, 'BTCUSD', 1000, 60000)

def signal_handler(sig, frame):
    trader.safe_exit()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)


while (True):
    # trader.feed_data(test = True)
    # trader.make_order(test = True)
    print("wait")
    time.sleep(1)

