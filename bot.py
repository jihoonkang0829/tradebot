from assets.algo import algo
from binance.client import Client
from binance.websockets import BinanceSocketManager
from twisted.internet import reactor
class Bot:
    def __init__(self, key, secret_key): 
        self.client = Client(api_key=key, secret_key=secret_key)
        self.decision = None
        self.position = None
        self.data = None
        self.begin = True

    def feed_data(self, symbol):
        if self.begin:
            socket
            self.begin = False
        # client get current data
        # client get current position
        # client get current balance 
        while(True):
            try:
                self.position = self.client.futures_position_information(symbol)
                self.data = self.client.
                break
            except:
                pass

    def btc_pairs_trade(msg):
        ''' define how to process incoming WebSocket messages '''
        if msg['stream'] != 'error':
            if len(price[symbol]) == 100000 :
                price[symbol] = pd.DataFrame(columns=['date', 'price'])
                error.to_csv(symbol + "error.csv")
            price[symbol].loc[len(price[symbol])] = [pd.Timestamp.now(), float(msg['data']['a'])]
        else:
            price['error']:True

        

    # def receive_decision(self):
    #     return self.decision

    def make_order(self): 
