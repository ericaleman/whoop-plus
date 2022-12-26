import os

from dotenv import load_dotenv
from pandasql import sqldf
import pandas as pd
import click

from clients import whoop
from utils import graphs

DAYS = 180

@click.group(chain=True)
def cli():
    pass

@cli.command('graph_trends')
@click.option('--metric',prompt=True)
def graph_trends(metric):

	# Generate trend graph
	file = open('queries/get_trends.sql', 'r')
	query = file.read()
	query = query.replace('{metric}', metric)
	result = pysqldf(query)
	graphs.blue_variance_graph(result, metric)

if __name__ == "__main__":

	# Open OAuth2 session for WHOOP API
	load_dotenv()
	USERNAME = os.getenv("USERNAME")
	PASSWORD = os.getenv("PASSWORD")
	whoop = whoop.Whoop(USERNAME, PASSWORD)

	# Get WHOOP data
	sleep = whoop.get_sleep_df(DAYS)
	cycle = whoop.get_cycle_df(DAYS)
	recovery = whoop.get_recovery_df(DAYS)

	# Setup query session
	pysqldf = lambda q: sqldf(q, globals())
	query_date_range = "SELECT min(cycle.day) as start_day FROM cycle"
	result = pysqldf(query_date_range)
	start_day = result['start_day'].iat[0]
	calendar = pd.DataFrame({'day':pd.date_range(start_day, periods=DAYS)})
	calendar['day'] = pd.to_datetime(calendar['day']).dt.date

	# Initialize CLI
	cli()






