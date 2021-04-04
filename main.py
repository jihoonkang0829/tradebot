from bot import Bot
from assets.credentials import *
from functions import *
import signal
import sys



trader = Bot(BINANCE_KEY, BIANCE_SECRET, 'BTCUSD', 1000)

signal.signal(signal.SIGINT, signal_handler)


while (True):
    trader.feed_data(test = True)
    trader.make_order(test = True)

