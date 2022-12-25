import json
from datetime import datetime, time, timedelta

from backoff import expo, on_exception
from ratelimit import RateLimitException, limits
import pandas as pd

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


class Whoop:

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
        if endpoint == 'cycle':
            days -= 1
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

    def get_cycle_df(self,days):
        """ 
        Returns a pandas DF for querying cycle data
        """
        collection = []
        nested_collection = self.get_collection(days,'cycle')
        for item in nested_collection:
            collection.append({
                    'id' : item['id'],   
                    'day' : datetime.fromisoformat(item['start'][:-1]).date(),
                    'start' : item['start'], 
                    'end' : item['end'], 
                    'timezone_offset' : item['timezone_offset'],   
                    'strain' : item['score']['strain'], 
                    'calories' : item['score']['kilojoule'] * 0.239006, 
                    'average_heart_rate' : item['score']['average_heart_rate'], 
                    'max_heart_rate' : item['score']['max_heart_rate'], 
                })  
        return pd.DataFrame.from_records(collection)

    def get_sleep_df(self,days):
        """ 
        Returns a pandas DF for querying sleep data
        """
        collection = []
        nested_collection = self.get_collection(days,'sleep')
        for item in nested_collection:
            collection.append({
                    'id' : item['id'], 
                    'start' : item['start'], 
                    'end' : item['end'], 
                    'timezone_offset' : item['timezone_offset'],   
                    'nap' : item['nap'],
                    'total_in_bed_time_milli' : item['score']['stage_summary']['total_in_bed_time_milli'], 
                    'total_awake_time_milli' : item['score']['stage_summary']['total_awake_time_milli'], 
                    'total_no_data_time_milli' : item['score']['stage_summary']['total_no_data_time_milli'], 
                    'total_light_sleep_time_milli' : item['score']['stage_summary']['total_light_sleep_time_milli'], 
                    'total_slow_wave_sleep_time_milli' : item['score']['stage_summary']['total_slow_wave_sleep_time_milli'], 
                    'total_rem_sleep_time_milli' : item['score']['stage_summary']['total_rem_sleep_time_milli'], 
                    'sleep_cycle_count' : item['score']['stage_summary']['disturbance_count'], 
                    'need_from_baseline_milli' : item['score']['sleep_needed']['baseline_milli'], 
                    'need_from_sleep_debt_milli' : item['score']['sleep_needed']['need_from_sleep_debt_milli'], 
                    'need_from_recent_strain_milli' : item['score']['sleep_needed']['need_from_recent_strain_milli'], 
                    'need_from_recent_nap_milli' : item['score']['sleep_needed']['need_from_recent_nap_milli'], 
                    'respiratory_rate' : item['score']['respiratory_rate'], 
                    'sleep_performance_percentage' : item['score']['sleep_performance_percentage'], 
                    'sleep_consistency_percentage' : item['score']['sleep_consistency_percentage'], 
                    'sleep_efficiency_percentage' : item['score']['sleep_efficiency_percentage'], 
                })  
        return pd.DataFrame.from_records(collection)

    def get_recovery_df(self,days):
        """ 
        Returns a pandas DF for querying recovery data
        """
        collection = []
        nested_collection = self.get_collection(days,'recovery')
        for item in nested_collection:
            collection.append({
                    'cycle_id' : item['cycle_id'], 
                    'sleep_id' : item['sleep_id'], 
                    'recovery_score' : item['score']['recovery_score'], 
                    'resting_heart_rate' : item['score']['resting_heart_rate'], 
                    'hrv_rmssd_milli' : item['score']['hrv_rmssd_milli'],
                    'spo2_percentage' : item['score']['spo2_percentage'], 
                    'skin_temp_celsius' : item['score']['skin_temp_celsius'], 
                })  
        return pd.DataFrame.from_records(collection)

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


