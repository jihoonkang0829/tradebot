import torch
from assets.model import RNNClassifier

# Algo/Bot
LEVERAGE_AMOUNT = 21
LOOKBACK = 15

# General
ASSETS_DIR = './assets/'
TEST_INITIAL_BALANCE = 100

# Model constants
INPUT_DIM = 1
HIDDEN_DIM = 32
NUM_LAYERS = 2
OUTPUT_DIM = 3