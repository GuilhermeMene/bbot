"""
A client code to connect with the Binance exchange
"""

import logger as log
from binance.spot import Spot
import time
import os

def get_debug_API(debug:bool):
    """
    Method to read API keys and Secret from env
    """

    if debug:
        api = {
        'api_key': os.environ.get('DEBUG_KEY'),
        'api_secret': os.environ.get('DEBUG_SECRET')
        }
    return api


class Client:

    def __init__(self, debug=False):

        try:
            if debug:
                self.api = get_debug_API(debug)
        except Exception as e:
            log.logger(e)

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

    def auth_client(self, key, secret):
        """
        Get an authenticated client for user endpoints
        """
        try:
            self.authClient = Spot(
                api_key=key,
                api_secret= secret
            )
            return self.authClient
        except Exception as e:
            log.logger(f"Authenticated Client error: {e}")

    def debug_client(self):
        """
        Get an authenticated client for debug and testing only
        """
        try:
            self.debugClient = Spot(
                api_key=self.api['api_key'],
                api_secret= self.api['api_secret'],
                base_url= 'https://testnet.binance.vision'
            )
            return self.debugClient
        except Exception as e:
            log.logger(f"Debug Client error: {e}")
