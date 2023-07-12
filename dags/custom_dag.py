from airflow import DAG
from datetime import datetime, timedelta
from sensors.my_airflow_sensor import MySensor
from operators.hello_operator import HelloOperator

default_args = {
	'owner': 'airflow',
	'depends_on_past': False,
	'start_date': datetime(2018, 1, 1),
	'email_on_failure': False,
	'email_on_retry': False,
	'retries': 1,
	'retry_delay': timedelta(minutes=5),
}


with DAG('customdag',
		 max_active_runs=3,
		 schedule_interval='@once',
		 default_args=default_args) as dag:

	sens = MySensor(
		task_id='SensorTask'
	)

	hello_task = HelloOperator(task_id='FollowupTask', name='foo_bar')



	sens >> hello_task