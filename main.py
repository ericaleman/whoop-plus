import os
from dotenv import load_dotenv

from pandasql import sqldf

from clients import whoop

load_dotenv()

USERNAME = os.getenv("USERNAME") or ""
PASSWORD = os.getenv("PASSWORD") or ""

if __name__ == "__main__":

	# Open OAuth2 session for WHOOP API
    whoop = whoop.Whoop(USERNAME, PASSWORD)

    # Get user information
    profile = whoop.get_profile_basic()
    body_measurements = whoop.get_body_measurement()

    # Get WHOOP data
    days = 30
    sleep_df = whoop.get_sleep_df(days)
    cycle_df = whoop.get_cycle_df(days)
    recovery_df = whoop.get_recovery_df(days)

    # Query data
    pysqldf = lambda q: sqldf(q, globals())
    query = "SELECT id FROM cycle_df"
    result = pysqldf(query)
    print(result)

