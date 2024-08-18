"""
A client code to connect with the Binance exchange
"""

from bbot import logger as log
from binance.spot import Spot
import time
import os

class Client:

    def __init__(self, debug=False):

        #Get the time from server and compare to local
        self.uclient = self.unauth_client()
        self.server_time = self.uclient.time()
        self.local_time = int(time.time())
        log.logger(f"Server time: {self.server_time} - Local time: {self.local_time}")

    def unauth_client(self):
        """
        Get an unauthenticated client for general purposes
        """
        try:
            unauthClient = Spot()
            return unauthClient
        except Exception as e:
            log.logger(f"Unauthenticated Client error: {e}")

    def auth_client(key, secret):
        """
        Get an authenticated client for user endpoints
        """
        try:
            authClient = Spot(
                api_key=key,
                api_secret= secret
            )
            return authClient
        except Exception as e:
            log.logger(f"Authenticated Client error: {e}")

    def debug_client(key, secret):
        """
        Get an authenticated client for debug and testing only
        """
        try:
            debugClient = Spot(
                api_key=key,
                api_secret= secret,
                base_url= 'https://testnet.binance.vision'
            )
            return debugClient
        except Exception as e:
            log.logger(f"Debug Client error: {e}")
