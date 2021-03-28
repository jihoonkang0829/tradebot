from constants import ASSETS_DIR
import pandas as pd
class BackTestDataLoader:
    def __init__(self):
        self.data = pd.read_csv(ASSETS_DIR + 'btctest.csv')