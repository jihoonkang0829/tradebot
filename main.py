from bot import Bot
from assets.credentials import *
import signal
import sys
import time

import torch
from constants import * 
from assets.gru import GRU


# trader = Bot(BINANCE_KEY, BINANCE_SECRET, 'BTCUSD', 1000, 60000)

# def signal_handler(sig, frame):
#     trader.safe_exit()
#     sys.exit(0)

# signal.signal(signal.SIGINT, signal_handler)

# test = True
# while (True):
#     trader.feed_data(test = test)
#     trader.make_order(test = test)

#     if test and trader.test_end_signal:
#         break
device = torch.device('cpu')
model = GRU(INPUT_DIM, HIDDEN_DIM, NUM_LAYERS, OUTPUT_DIM)
model.load_state_dict(torch.load(ASSETS_DIR + 'gru_classification_model.pt', map_location=device))
model.eval()
print('success')
