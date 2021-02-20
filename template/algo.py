from typing import Tuple

def algo(current_data = list, balance = float, position = int) -> Tuple(int, str, int, bool, int, float):
    '''
    Function to make decision

    Params
    ———
    current_data: list
        real time data

    balance: float
        current user balance
    
    int:
        0: Buy
        1: Sell
        2: Do nothing (Neutral)

    Returns
    ———
    int:
        epoch time

    str:
        symbol(ticker)

    int:
        0: Buy
        1: Sell
        2: Do nothing (Neutral)
    int:
        leverage

    bool:
        True: MKTPC
        False: limit price
    
    int:
        limit price, None if MKTPC

    float:
        quantity to buy/sell
    '''