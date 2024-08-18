"""
Author: Guilherme Mene Ale Primo
Date: 08/09/2024
bbot - A Binance bot for Spot trade BTCUSDT
"""

import os
import sys
import time
import pandas as pd
from bbot import logger as log
from bbot.client import Client
from bbot import connection_checker as con
from bbot import strategy
from binance.spot import Spot
from binance.error import ClientError


class Bbot:

    def __init__(self, debug=False):

        #Set the variables
        self.symbol = 'BTCUSDT'
        self.logged = False
        self.operational = False

        #Get token
        if not debug:
            self.key = os.environ.get('BBOT_KEY')
            self.secret = os.environ.get('BBOT_SECRET')
        if debug:
            self.key = os.environ.get('DEBUG_KEY')
            self.secret = os.environ.get('DEBUG_SECRET')

        #Get the client for trade
        if debug:
            self.client = Client.debug_client(key=self.key, secret=self.secret)
            self.logged = True
        else:
            self.client = Client.auth_client(key=self.key, secret=self.secret)
            self.logged = True

        #Get the ping of binance
        self.ping = con.get_ping()
        if self.ping < 1:
            self.operational = True

    def runTask(self):
        """
        Method to run the bot on a loop
        """
        while True:
            from bbot.telegram_bot import STATE
            if STATE == 0:
                self.cancel_orders()
                log.logger("Stopping the bot.")
                continue
            else:
                log.status_logger(f"Operational state: {self.operational} : Ping: {self.ping}")
                self.runBot()

    def runBot(self):
        """
        Method to run the pipeline of the Binance Spot Trade Bot.
        The pipeline is:
        1. get balances;
        2. get klines;
        3. run strategy to define: sell or buy;
        4. get ticker price and average price;
        5. set the params of order;
        6. make order.
        """

        #Get the balances and save in database
        print("Starting task...")
        btc, usdt = self.get_balances()
        log.balance_logger(asset='BTC', balance=btc)
        log.balance_logger(asset='USDT', balance=usdt)

        #Get the klines
        self.get_klines()

        #Get the ticker price
        self.ticker = float(self.client.ticker_price(self.symbol)['price'])

        #Calculate the indicators
        self.typeOrder = strategy.getStrategy(self.klines)
        #Make order
        orderQty = self.calcQty()

        if self.typeOrder != 'Neutral' and self.doTrade:
            self.params = {
                'symbol': self.symbol,
                'side': self.typeOrder,
                'type': 'MARKET',
                'timeInForce': 'GTC',
                'quantity': orderQty,
            }
            #Make order
            try:
                print(f"Making {self.typeOrder} order...")
                response = self.make_order()
                log.trade_logger(response=response)
            except Exception as e:
                log.logger(e)

    def calcQty(self):
        """
        Calculate the quantity of the order
        """
        self.doTrade = False
        if self.typeOrder == 'SELL':
            if self.btc_balance > 0.000001:
                self.doTrade = True
                return float(self.btc_balance)
            else:
                self.doTrade = False
        else:
            buy_amount = float((self.usdt_balance / self.ticker)*0.95)
            if buy_amount > 0.000001:
                self.doTrade = True
                return buy_amount
            else:
                self.doTrade = False


    def get_klines(self):
        """
        Get the klines to calculate the indicators
        """
        try:
            klines = self.client.klines(symbol=self.symbol, interval="1m", limit=60)

            column_names = ['OpenTime','Open','High','Low','Close','Volume','CloseTime',
                            'qAssetVol','Ntrades','TbuybAssetVol','TbuyqAssetVol','Ignore']
            dtypes = {'OpenTime':'int32',
                      'Open':'float32',
                      'High':'float32',
                      'Low':'float32',
                      'Close':'float32',
                      'Volume':'float32',
                      'CloseTime':'int32',
                      'qAssetVol':'float32',
                      'Ntrades':'int32',
                      'TbuybAssetVol':'float32',
                      'TbuyqAssetVol':'float32',
                      'Ignore':'int32'}
            self.klines = pd.DataFrame(klines, columns=column_names)
            self.klines = self.klines.astype(dtype=dtypes)
        except Exception as e:
            log.logger(e)

    def get_balances(self):
        """
        Get the balance from account
        """
        try:
            self.acc_details = self.client.account(omitZeroBalances="true")
            self.balances = self.acc_details['balances']

            #Get only the BTC and USDT balances
            for coin in self.balances:
                if coin['asset'] == 'BTC':
                    self.btc_balance = float(coin['free'])
                elif coin['asset'] == 'USDT':
                    self.usdt_balance = float(coin['free'])
        except Exception as e:
            log.logger(e)

        return self.btc_balance, self.usdt_balance

    def make_order(self):
        """
        Create market long order
        """
        try:
            resp = self.client.new_order(**self.params)
            log.trade_logger(resp)
        except ClientError as error:
            log.error_log(error)

    def cancel_orders(self):
        """
        Cancel openned orders
        """
        try:
            resp = self.client.cancel_open_orders(symbol=self.symbol)
            log.logger("Cancelling the openned order.")
        except ClientError as error:
            log.error_log(error)

#Run the bot
if __name__ == '__main__':
    from threading import Thread
    from bbot import telegram_bot

    #Check the sys args
    if len(sys.argv) > 1:
        if sys.argv[1] == "debug":
            bbot = Bbot(debug=True)
    else:
        bbot = Bbot()

    #Run the bot using 1 minute interval
    while True:

        hold_threading = True

        threads=[]
        print("*** Creating bot threads... ")

        t = Thread(target=bbot.runTask)
        t.start()
        threads.append(t)

        print("*** Joining threads...")
        hold_threading = False
        for t in threads:
            t.join()

        current_time = time.localtime()
        current_time = time.strftime("%H:%M:%S", current_time)
        print(f"Time: {current_time}")

        print("*** Sleeping...")
        time.sleep(65)






