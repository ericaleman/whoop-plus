from __future__ import annotations

import json
from datetime import datetime, time, timedelta
from typing import Any
from backoff import expo, on_exception
from ratelimit import RateLimitException, limits

from authlib.common.urls import extract_params
from authlib.integrations.requests_client import OAuth2Session


AUTH_URL = "https://api-7.whoop.com"
REQUEST_URL = "https://api.prod.whoop.com/developer"
TOKEN_ENDPOINT_AUTH_METHOD = "password_json"
RATE_LIMITS = {
    "calls": 100,  # of calls per rate limit period
    "period": 60,  # number of seconds in rate limit period
}
HEADERS = {
    "Content-Type": "application/json",
}


def _auth_password_json(_client, _method, uri, headers, body):
    body = json.dumps(dict(extract_params(body)))
    headers["Content-Type"] = "application/json"
    return uri, headers, body


class WhoopClient:

    
    def __init__(self,username,password):
        self._username = username
        self._password = password
        self.user_id = ""
        self.session = OAuth2Session(
            token_endpont=f"{AUTH_URL}/oauth/token",
            token_endpoint_auth_method=TOKEN_ENDPOINT_AUTH_METHOD,
        )
        self.session.register_client_auth_method(
            (TOKEN_ENDPOINT_AUTH_METHOD, _auth_password_json)
        )

        self.auth()

    def get_profile_basic(self):
        """ 
        Returns your user profile:
        """
        return self.get(url=f"{REQUEST_URL}/v1/user/profile/basic")

    def get_body_measurement(self):
        """ 
        Returns your user body measurements:
        """
        return self.get(url=f"{REQUEST_URL}/v1/user/measurement/body")

    def get_collection(self,days, endpoint):
        """ 
        Returns last N daily WHOOP scores descending from most recent:
        """
        start = (datetime.today() - timedelta(days=days)).isoformat() + "Z"
        end = datetime.today().isoformat() + "Z"

        urls = {
            "cycle" : f"{REQUEST_URL}/v1/cycle",
            "recovery" : f"{REQUEST_URL}/v1/recovery",
            "sleep" : f"{REQUEST_URL}/v1/activity/sleep",
            "workout" : f"{REQUEST_URL}/v1/activity/workout"
        }
        collection = self.get_paginate(
            url=urls[endpoint],
            params={"start": start, "end": end, "limit": 25},
        )

        return collection

    def auth(self, **kwargs):
        """
        Authenticate OAuth2Session
        """
        self.session.fetch_token(
            url=f"{AUTH_URL}/oauth/token",
            username=self._username,
            password=self._password,
            grant_type="password",
            **kwargs,
        )

        if not self.user_id:
            self.user_id = str(self.session.token.get("user", {}).get("id", ""))

    def get(self, url, **params):

        def run_request(method, url):
            response = self.session.request(method="GET", url=url, **params)
            if response.status_code not in [200, 429]:
                response.raise_for_status()
            return response.json()

        @on_exception(expo, RateLimitException, max_tries=8)
        @limits(calls=RATE_LIMITS["calls"], period=RATE_LIMITS["period"])
        def rate_limiter(*args, **kwargs):
            return run_request(url, *args, **kwargs)

        return rate_limiter(url)

    def get_paginate(self, url, **kwargs):
        params = kwargs.pop("params", {})
        responses = []

        while True:
            response = self.get(url=url,params=params,**kwargs)
            responses += response["records"]
            if next_token := response["next_token"]:
                params["nextToken"] = next_token
            else:
                break

        return responses


