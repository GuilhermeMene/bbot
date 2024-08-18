"""
A datalog for the trade bot operations
"""

import os
import time

directory = os.getcwd()
op_log = os.path.join(directory, 'Op-logs.txt')
trade_log = os.path.join(directory, 'Trade-logs.csv')
balance_log = os.path.join(directory, 'Balance-logs.csv')

def logger(log:str):
    """
    Datalog for operational events only
    """

    logtime = str(int(time.time()))

    with open(op_log, 'a') as opl:
        opl.write(f"{logtime}: {log} \n")
        opl.close()

def status_logger(log:str):
    """
    Status log method
    """
    logtime = str(int(time.time()))

    with open(os.path.join(directory, 'Status-logs.txt'), 'a') as stl:
        stl.write(f"{logtime}: {log} \n")
        stl.close()

def error_log(error):
    """
    Error log method
    """
    error = f"Error found: status: {error.status_code}, error code: {error.error_code}, and error message: {error.error_message}"
    logger(error)


def trade_logger(response):
    """
    Datalog of trades and responses from submitted orders
    """
    try:
        #Write a csv file
        logtime = str(int(time.time()))

        head = f"Time, Symbol, ClientOrderId, Price, origQty, execQty, Type, Side"
        line = f"{logtime}, {response['symbol']}, {response['clientOrderId']}, {response['price']}, \
                {response['origQty']},{response['executedQty']}, {response['type']}, {response['side']}"

        if os.path.exists(trade_log):
            with open(trade_log, 'a') as tl:
                tl.write(line + "\n")
        else:
            with open(trade_log, 'a') as tl:
                tl.write(head + "\n")
                tl.write(line + "\n")

    except Exception as e:
        logger(f"Trade logger error: {e}")

def balance_logger(asset:str, balance:float):
    """
    Save the asset balances in the database
    """
    try:
        #Write the balance to csv
        logtime = str(int(time.time()))

        head = f"Time, Asset, Balance"
        line = f"{logtime}, {asset}, {balance}"

        if os.path.exists(balance_log):
            with open(balance_log, 'a') as bl:
                bl.write(line + "\n")
        else:
            with open(balance_log, 'a') as bl:
                bl.write(head + "\n")
                bl.write(line + "\n")

    except Exception as e:
        logger(f"Balance logger error: {e}")

def get_last_trade():
    """
    Get the last trade from database
    """

    try:
        with open(trade_log, 'r') as trade:
            for line in trade:
                pass
            last_trade = list(line.split(','))

        return last_trade

    except Exception as e:
        logger(e)
