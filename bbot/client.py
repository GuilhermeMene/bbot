"""
A client code to connect with the Binance exchange
"""

import logger as log
from binance.spot import Spot
import time

def get_API(debug:bool):
    """
    Method to read API keys and Secret from env
    """

    if debug:
        envfile = "../env/.debugenv"
    else:
        envfile = "../env/.env"

    with open(envfile, "r") as env:
        line = env.readline()
        env.close

    api_key = line.split(',')[0]
    api_secret = line.split(',')[1]

    api = {
        'api_key': api_key,
        'api_secret': api_secret
    }
    return api


class Client:

    def __init__(self, debug=False):

        try:
            self.api = get_API(debug)
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

    def auth_client(self):
        """
        Get an authenticated client for user endpoints
        """
        try:
            self.authClient = Spot(
                api_key=self.api['api_key'],
                api_secret= self.api['api_secret']
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
