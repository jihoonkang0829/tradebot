from constants import ASSETS_DIR
from assets.algo import *
from functions import *
from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceOrderException
from binance.websockets import BinanceSocketManager
from time import sleep
import time
import pandas as pd

# Model import
from assets.model import RNNClassifier

class Bot:
    def __init__(self, key, secret_key, symbol, deltatime, algodelay, test = False): 
        self.client = Client(api_key=key, api_secret=secret_key)
        self.decision = None
        self.symbol = str(symbol)
        self.cur_price = 0
        self.socket_error = None
        self.position = 0
        self.balance = 0
        self.deltatime = deltatime
        self.algodelay = algodelay
        self.prev_algo_execute = time.time()
        self.test = test
        if not self.test:
            self.start_socket()
            while True:
                try:
                    self.position = str(self.client.futures_position_information(symbol = symbol))
                    self.balance = float(self.client.futures_account_balance()[0]['balance'])
                    break
                except BinanceAPIException as e:
                    print(e, "curpos")
                    pass
                except BinanceOrderException as e:
                    print(e, "curpos")
                    pass
        else:
            self.test_data = pd.read_csv(ASSETS_DIR + 'BTCUSDTMIN.csv')
            self.test_index = 0

    def start_socket(self):
        # start socket and save the key
        self.bsm = BinanceSocketManager(self.client)
        self.conn_key = self.bsm.start_symbol_ticker_futures_socket(self.symbol, self.btc_pairs_trade)
        self.bsm.start()
        self.begin = False
        while self.cur_price == 0:
            sleep(0.1)
        
    def btc_pairs_trade(self, msg):
        if msg['stream'] != 'error':
            self.cur_price = float(msg['data']['a'])
        else:
            self.socket_error = True

    def feed_data(self):
        # In Deploy mode
        if not self.test:
            if time.time() - self.algodelay > self.prev_algo_execute:
                self.prev_algo_execute = time.time()
                while(True):
                    try:
                        self.position = dict(self.client.futures_position_information(symbol = self.symbol)[0])
                        self.balance = float(self.client.futures_account_balance()[0]['balance'])
                        break
                    except:
                        pass

                if self.socket_error:
                    self.socket_error = False
                    self.bsm.stop_socket(self.conn_key)
                    self.bsm.start()
                    return
            
        # In Test mode
        else:
            self.cur_price = self.test_data.iloc[self.test_index, :]['']
            self.position = self.decision

            # self.cir_price: float
            # self.balance: float
            # self.position: dict
        self.position = convert_dict_value_type(self.position, 'float')
        self.decision = algo(self.cur_price, self.balance, self.position)
        #{timestamp, symbol, action, leverage, price_type, price, quantity}
    def make_order(self, test : bool = False):
        # convert time.time sec to milisec
        if int(time.time()*1000) - self.decision['timestamp']  > self.deltatime:
            return
        if self.decision['action'] == 2:
            return
        if self.decision['action'] == 0:
            # if "BUY"
            if self.decision['price_type'] == "MARKET":
                while True:
                    try:
                        self.client.futures_change_leverage(symbol = self.symbol, leverage = self.decision['leverage'])
                        self.client.futures_create_order(symbol = self.symbol, side = "BUY", type = "MARKET",quantity= self.decision['quantity'])
                        break
                    except BinanceAPIException as e:
                        print(e, "leverage api")
                        pass
                    except BinanceOrderException as e:
                        print(e, "leverage order")
                        pass            
            elif self.decision['price_type'] == "LIMIT":
                while True:
                    try:
                        self.client.futures_change_leverage(symbol = self.symbol, leverage = self.decision['leverage'])
                        self.client.futures_create_order(symbol = self.symbol, side = "BUY", type = "LIMIT", price = self.decision['price'], quantity= self.decision['quantity'])
                        break
                    except BinanceAPIException as e:
                        print(e, "leverage api")
                        pass
                    except BinanceOrderException as e:
                        print(e, "leverage order")
                        pass
        elif self.decision['action'] == 1:
            # if "SELL"
            if self.decision['price_type'] == "MARKET":
                while True:
                    try:
                        self.client.futures_change_leverage(symbol = self.symbol, leverage = self.decision['leverage'])
                        self.client.futures_create_order(symbol = self.symbol, side = "SELL", type = "MARKET", quantity= self.decision['quantity'])
                        break
                    except BinanceAPIException as e:
                        print(e, "leverage api")
                        pass
                    except BinanceOrderException as e:
                        print(e, "leverage order")
                        pass            
            elif self.decision['price_type'] == "LIMIT":
                while True:
                    try:
                        self.client.futures_change_leverage(symbol = self.symbol, leverage = self.decision['leverage'])
                        self.client.futures_create_order(symbol = self.symbol, side = "SELL", type = "LIMIT", price = self.decision['price'], quantity= self.decision['quantity'])
                        break
                    except BinanceAPIException as e:
                        print(e, "leverage api")
                        pass
                    except BinanceOrderException as e:
                        print(e, "leverage order")
                        pass   
    def safe_exit(self):
        self.feed_data()

        if self.position['positionSide'] == 'BOTH':
            return

        if self.position['positionSide'] == 'LONG': 
            self.client.futures_create_order(symbol = self.symbol, 
                                            side = "SELL", 
                                            type = "MARKET", 
                                            quantity= round_decimals_down(float(self.position['positionAmt'])), 
                                            reduceOnly = True)

        if self.position['positionSide'] == 'SHORT':
            self.client.futures_create_order(symbol = self.symbol, 
                                            side = "BUY", 
                                            type = "MARKET", 
                                            quantity= round_decimals_down(float(self.position['positionAmt'])), 
                                            reduceOnly = True)
        