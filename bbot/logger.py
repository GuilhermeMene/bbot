"""
A datalog for the trade bot operations
"""

import os
import sqlite3 as sql
import time

directory = os.getcwd()
op_log = os.path.join(directory, 'Op-logs.txt')

database = os.path.join(directory, 'Log_database.db')

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

    with open(os.path.join(directory, 'Status-logs.txt'), 'r') as stl:
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
        #Connect to the database
        con = sql.connect(database=database)
        cursor = con.cursor()

        logtime = str(int(time.time()))

        #Execute the script
        cursor.executescript(f'''CREATE TABLE IF NOT EXISTS trades (Id INT PRIMARY KEY AUTOINCREMENT,
                             Time INT NOT NULL,
                             Symbol VARCHAR NOT NULL,
                             ClientOrderId VARCHAR NOT NULL,
                             Price REAL NOT NULL,
                             origQty RAL NOT NULL,
                             execQty REAL NOT NULL,
                             Type VARCHAR NOT NULL,
                             Side VARCHAR NOT NULL);
                             INSERT OR IGNORE INTO trades ({logtime}, {response['symbol']},
                             {response['clientOrderId']}, {response['price']}, {response['origQty']},
                             {response['executedQty']}, {response['type']}, {response['side']});''')
        con.commit()
        con.close()
    except Exception as e:
        logger(e)

def balance_logger(asset:str, balance:float):
    """
    Save the asset balances in the database
    """
    try:
        #Connect to the database
        con = sql.connect(database=database)
        cursor = con.cursor()

        logtime = str(int(time.time()))

        #Execute the script
        cursor.executescript(f'''CREATE TABLE IF NOT EXISTS balances (Id INT PRIMARY KEY AUTOINCREMENT,
                             Time INT NOT NULL,
                             Asset VARCHAR NOT NULL,
                             Balance REAL NOT NULL);
                             INSERT OR IGNORE INTO balances ({logtime}, {asset}, {balance})''')
        con.commit()
        con.close()
    except Exception as e:
        logger(e)

def get_last_trade():
    """
    Get the last trade from database
    """

    try:
        #Conenct to the database
        con = sql.connect(database=database)
        cursor = con.cursor()

        #get the last trade
        cursor.execute("SELECT * FROM trades ORDER BY Id DESC LIMIT 1")
        last_trade = cursor.fetchone()

        con.commit()
        con.close()

        return last_trade

    except Exception as e:
        logger(e)
