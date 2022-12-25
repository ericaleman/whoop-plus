import os
from dotenv import load_dotenv

import pandas as pd

from clients import whoop

load_dotenv()

USERNAME = os.getenv("USERNAME") or ""
PASSWORD = os.getenv("PASSWORD") or ""

if __name__ == "__main__":

	# Open OAuth2 session for WHOOP API
    client = whoop.WhoopClient(USERNAME, PASSWORD)

    # Get user information
    profile = client.get_profile_basic()
    body_measurements = client.get_body_measurement()

    # Get collection
    collection = client.get_collection(30, 'cycle')
    df = pd.DataFrame.from_records(collection)
