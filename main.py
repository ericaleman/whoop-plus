import os

from dotenv import load_dotenv
from pandasql import sqldf
import pandas as pd
import click

from clients import whoop
from utils import graphs

DAYS = 30

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

	"""
	Allows you to graph trends for any of the following metrics:

		strain,
		calories,

		average_heart_rate,
		max_heart_rate,
		resting_heart_rate,

		respiratory_rate,
		hrv_rmssd_milli, 
		spo2_percentage,

		skin_temp_celsius,

		total_in_bed_time_milli,
		total_awake_time_milli,
		total_no_data_time_milli,
		total_light_sleep_time_milli, 
		total_slow_wave_sleep_time_milli, 
		total_rem_sleep_time_milli, 
		sleep_cycle_count, 

		need_from_baseline_milli,
		need_from_sleep_debt_milli,
		need_from_recent_strain_milli,
		need_from_recent_nap_milli,
		
		sleep_performance_percentage,
		sleep_consistency_percentage,
		sleep_efficiency_percentage

	"""
	
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






