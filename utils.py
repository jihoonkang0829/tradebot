from constants import KLINES_VALID_INTERVALS
import time
import math
import numpy as np
import datetime

def convert_dict_value_type(d: dict, type_str: str) -> dict:
    """
    Function to convert the value type of the passed dictionary

    Params
    ------
    d: dict
        parameter dictionary to be converted

    type_str: str
        type of value to be converted. Can only be 'str', 'int', 'float', 'list'

    Returns
    -------
    dict:
        value-converted dict
    """

    if type_str not in ['str', 'int', 'float', 'list']:
        print("Cannot be converted to the passed type.\ntype_str must be 'str', 'int', 'float' or 'list'.")
        return d

    if not isinstance(d, dict):
        print("d must be dict.")
        return d

    if type_str == 'str':
        return {key : str(val) for key, val in d.items()}

    if type_str == 'int':
        return {key : int(val) for key, val in d.items()}

    if type_str == 'float':
        return {key : float(val) for key, val in d.items()}

    if type_str == 'list':
        return {key : list(val) for key, val in d.items()}

    return d

def round_decimals_down(number:float, decimals:int=3) -> float:
    """
    Returns a value rounded down to a specific number of decimal places.
    """
    if not isinstance(decimals, int):
        raise TypeError("decimal places must be an integer")
    elif decimals < 0:
        raise ValueError("decimal places has to be 0 or more")
    elif decimals == 0:
        return math.floor(number)

    factor = 10 ** decimals
    return math.floor(number * factor) / factor

def curtime():
    """
    Returns current time in milliseconds
    """
    return time.time() * 1000

def test_update_balance_start_position():
    """
    Update test mode position start balance
    """
    return 0

def test_update_balance_end_position(cur_balance, pos_decision, pos_start_price, pos_end_price, pos_amount, lev_amount):
    """
    Update test mode position end balance
    """
    assert pos_decision in [0, 1, 2]

    abs_delta = np.abs(pos_end_price - pos_start_price) * pos_amount * lev_amount
    if pos_decision == 0:
        if pos_end_price - pos_start_price > 0:
            return cur_balance + abs_delta
        else:
            return max(0, cur_balance - abs_delta)
    elif pos_decision == 1:
        if pos_end_price - pos_start_price < 0:
            return cur_balance + abs_delta
        else:
            return max(0, cur_balance - abs_delta)

    else:
        return cur_balance

# Data retrieving modules

def get_klines_data(client, symbol, start, end, interval):
    if interval not in KLINES_VALID_INTERVALS:
        print('Input interval is not valid.')
        return None

    def str_or_datetime(dt):
        return isinstance(dt, str) or isinstance(dt, datetime.datetime)

    def todatetime(dt):
        if isinstance(dt, datetime.datetime):
            return dt

        return datetime.datetime.strptime(dt, '%Y-%m-%d')

    if not str_or_datetime(start):
        print('start datetime is not valid')
        return None

    if not str_or_datetime(end):
        print('end datetime is not valid')
        return None

    start, end = todatetime(start), todatetime(end)

    if start > end:
        print('start date must be earlier than end date')
        return None

    if end > datetime.datetime.now():
        print('end date must be earlier than current time')
        return None

    return client.futures_klines(symbol = symbol,
                                interval = interval,
                                startTime = start,
                                endTime = end)

    
