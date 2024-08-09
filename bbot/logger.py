"""
A datalog for the trade bot operations
"""

import datetime
import os
import sqlite3

directory = os.getcwd()
op_log = os.path.join(directory, 'Op-logs.txt')

def logger(log:str):
    """
    Datalog for operational events only
    """

    time = str(datetime.datetime.now())

    with open(op_log, 'a') as opl:
        opl.write(f"{time}: {log} \n")
        opl.close


def error_log(error):
    """
    Error log method
    """
    error = f"Error found: status: {error.status_code}, error code: {error.error_code}, and error message: {error.error_message}"
    logger(error)


def trade_logger(response, params):
    """
    Datalog of trades and responses from submitted orders
    """
    print("Trade logs will implemented!")

def balance_logger():
    """
    Datalog of balance
    """
    print("Trade logs will implemented!")

