import requests
import hashlib
from uuid import uuid4
from urllib.parse import urlencode

import jwt


def get_all_markets(is_details=False):
    url = "https://api.upbit.com/v1/market/all"
    parameters = {"isDetails": is_details}
    return requests.get(url, parameters).json()


def get_minute_candles(market, unit, to=None, count=None):
    url = f"https://api.upbit.com/v1/candles/minutes/{unit}"  # f-string

    parameters = {"market": market}
    if to is not None:
        paramters["to"] = to
    if count is not None:
        parameters["count"] = count

    return requests.get(url, parameters).json()


class Client:

    def __init__(self, access_key, secret_key):
        self.access_key = access_key
        self.secret_key = secret_key
        if not self.is_valid_key():
            raise InvalidKeyError("올바른 키가 아닙니다")

    def _hash_parameters(self, parameters):
        encoded = urlencode(parameters).encode()
        m = hashlib.sha512()
        m.update(encoded)
        return m.hexdigest()

    def _make_authorization_token(self, parameters=None):
        payload ={
            "access_key": self.access_key,
            "nonce": str(uuid4())
        }

        if parameters is not None:
            payload["query_hash"] = self._hash_parameters(parameters)
            payload["hash_alg"] = "SHA512"

        return jwt.encode(payload, self.secret_key)

    def _get_authorization_headers(self, parameters=None):
        token = self._make_authorization_token(parameters)
        return {"Authorization": f"Bearer {token}"}

    def is_valid_key(self):
        url = "https://api.upbit.com/v1/api_keys"
        response = requests.get(url, headers=self._get_authorization_headers()).json()
        return "error" not in response

    def get_order_chance(self, market):
        url = "https://api.upbit.com/v1/orders/chance"
        parameters = {"market": market}
        headers = self._get_authorization_headers(parameters)
        return requests.get(url, parameters, headers=headers).json()
        

class InvalidKeyError(Exception):
    pass
