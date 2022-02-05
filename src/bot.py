from constants import ASSETS_DIR
from algo import *
from utils import *
from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceOrderException
from binance.websockets import BinanceSocketManager
from time import sleep
import pandas as pd
import os


class Bot:
    def __init__(self, symbol, deltatime, algodelay, test = False, api_key = "", api_secret = ""): 

        if api_key == "" or api_secret == "":
            self.initialize()
        else:
            self.initialize(api_key, api_secret)

        self.client = Client(api_key=api_key, api_secret=api_secret)
        self.decision = None
        self.symbol = str(symbol)
        self.cur_price = 0
        self.socket_error = None
        self.position =  dict({'timestamp' : time.time(),
                                'symbol'     : symbol,
                                'action'     : 2,
                                'leverage'   : 1,
                                'price_type' : 'MKTPC',
                                'price'      : None,
                                'quantity'   : None})
        self.balance = 0
        self.deltatime = deltatime
        self.algodelay = algodelay

        # test attributes
        self.prev_algo_execute = 0
        self.test = test
        self.pos_start_price = 0
        self.has_position = False
        self.test_end_signal = False

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

        # Test mode
        else:
            self.test_data = pd.read_csv(ASSETS_DIR + 'BTCUSDTMIN.csv')
            self.test_index = 0
            self.balance = TEST_INITIAL_BALANCE

    def initialize(self, api_key : str, api_secret : str):
        self.client = Client(api_key, api_secret)

    def initialize(self):
        api_key = os.getenv('BINANCE_KEY')
        api_secret = os.getenv('BINANCE_SECRET')
        if api_key == '' or api_secret == '':
            print("Please set BINANCE_KEY and BINANCE_SECRET environment variables")
            exit(1)
        self.client = Client(api_key, api_secret)

    def start_socket(self):
        # start socket and save the api_key
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
            if curtime() - self.algodelay > self.prev_algo_execute:
                self.prev_algo_execute = curtime()
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
                self.position = convert_dict_value_type(self.position, 'float')
                self.decision = algo(self.cur_price, self.balance, self.position)
            
        # In Test mode
        else:
            if self.test_index == len(self.test_data):
                self.test_end_signal = True
                
            self.cur_price = self.test_data.iloc[self.test_index, :]['open']
            self.test_index += 1
            self.position = self.decision
            self.decision = algo(self.cur_price, self.balance, self.position)

        
        #{timestamp, symbol, action, leverage, price_type, price, quantity}
    def make_order(self):
        if not self.test:
            # convert time.time sec to millisec
            if curtime() - self.decision['timestamp']  > self.deltatime:
                return
            if self.decision['action'] == 2:
                return
            if self.decision['action'] == 0:
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

        # TODO: Update test mode balance calculation logic
        else:
            if self.decision['action'] != 2 and not self.has_position:
                self.balance = test_update_balance_start_position()
                self.pos_start_price = self.cur_price
                self.has_position = True
                self.position = self.decision
            elif self.decision['action'] != 2 and self.has_position and self.position['action'] != self.decision['action']:
                self.balance = test_update_balance_end_position(self.balance, 
                                                                self.decision['action'], 
                                                                self.pos_start_price, 
                                                                self.cur_price, 
                                                                self.decision['quantity'], 
                                                                self.decision['leverage'])
                self.has_position = False
                print(self.balance)

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
        