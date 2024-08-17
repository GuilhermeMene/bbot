"""
Connection checker for network stability and latency
"""

import httpx
from bbot import logger as log

base_url = 'https://api.binance.com'
endpoint = '/api/v3/ping'

def get_ping():
    try:
        with httpx.Client() as client:
            resp = client.get(base_url+endpoint)
            return resp.elapsed.total_seconds()
    except Exception as e:
        log.logger(e)
