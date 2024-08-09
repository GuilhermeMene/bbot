"""
Author: Guilherme Mene Ale Primo
Date: 08/09/2024
bbot - A Binance bot for Spot trade BTCUSDT
"""

from bbot import logger as log
from bbot.client import Client
from bbot import connection_checker as con
from binance.spot import Spot
from binance.error import ClientError


class Bbot:

    def __init__(self, debug=False):

        #Set the variables
        self.operational = False

        try:
            if debug:
                self.client = Client()
                self.client = self.client.debug_client
            else:
                self.client = Client()
                self.client = self.client.auth_client
        except Exception as e:
            log.logger(e)

        try:
            self.ping = con.get_ping()
            if self.ping < 1:
                self.operational = True
        except Exception as e:
            log.logger(e)

    def make_order(self):
        """
        Create market long order
        """
        try:
            resp = self.client.new_order(**self.order_params)
            log.trade_logger(resp, self.order_params)
        except ClientError as error:
            log.error_log(error)

    def cancel_order(self):
        """
        Create market long order
        """
        try:
            resp = self.client.new_order(**self.cancel_params)
            log.trade_logger(resp, self.cancel_params)
        except ClientError as error:
            log.error_log(error)







"""
Pseudo algo:

Main pipeline
1. Get the signal from latency checker
2. Get balance (free) and save the balance (SQLite)
3. Get klines
4. Calculate the indicators
5. Check if long or short based on the balance and indicators
6. Make order (long or short) and save the trade (SQLite)
7. Sleep the period

Telegram bot pipeline (append thread)
1. Sign
2. Get the client
3. Run background to receive the commands:
    - check status
    - get trades
    - get balance
    - print trades or not trades

Latency and stability of network
1. Check the connection with internet
2. Check the latency from Binance
3. Send signal to bot to wait or continue operations
"""
