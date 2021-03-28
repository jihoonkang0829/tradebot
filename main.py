from bot import Bot
from assets.credentials import *



trader = Bot(BINANCE_KEY, BIANCE_SECRET, 'BTCUSD', 1000)

while (True):
    trader.feed_data(test = True)
    trader.make_order(test = True)


trader = bot(key, secret_key)
while True():
    trader.feed_data()
