"""
client.py — Binance Futures Testnet API wrapper
Handles authentication and raw HTTP communication with the Binance Futures Testnet.
"""

import time
import hmac
import hashlib
import requests
from urllib.parse import urlencode
from bot.logging_config import get_logger

logger = get_logger(__name__)

BASE_URL = "https://testnet.binancefuture.com"


class BinanceClient:
    def __init__(self, api_key: str, api_secret: str):
        self.api_key = api_key
        self.api_secret = api_secret
        self.session = requests.Session()
        self.session.headers.update({
            "X-MBX-APIKEY": self.api_key,
            "Content-Type": "application/json"
        })
        logger.info("BinanceClient initialized (Futures Testnet)")

    def _sign(self, params: dict) -> dict:
        """Add HMAC SHA256 signature to request params."""
        params["timestamp"] = int(time.time() * 1000)
        query_string = urlencode(params)
        signature = hmac.new(
            self.api_secret.encode("utf-8"),
            query_string.encode("utf-8"),
            hashlib.sha256
        ).hexdigest()
        params["signature"] = signature
        return params

    def get(self, endpoint: str, params: dict = None, signed: bool = False) -> dict:
        """Make a GET request."""
        params = params or {}
        if signed:
            params = self._sign(params)
        url = BASE_URL + endpoint
        logger.debug(f"GET {url} | params: {params}")
        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.Timeout:
            logger.error("Request timed out.")
            raise
        except requests.exceptions.ConnectionError:
            logger.error("Network connection error.")
            raise
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP error: {e} | Response: {response.text}")
            raise

    def post(self, endpoint: str, params: dict = None, signed: bool = True) -> dict:
        """Make a POST request."""
        params = params or {}
        if signed:
            params = self._sign(params)
        url = BASE_URL + endpoint
        logger.debug(f"POST {url} | params: {params}")
        try:
            response = self.session.post(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.Timeout:
            logger.error("Request timed out.")
            raise
        except requests.exceptions.ConnectionError:
            logger.error("Network connection error.")
            raise
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP error: {e} | Response: {response.text}")
            raise
