from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime

# Define your Python functions
def get_artists():
    # Your Python code here

def get_albums():
    # Your Python code here

def get_songs():
    # Your Python code here

# Define the DAG
dag = DAG(
    'HH_dag',
    start_date=datetime(2023, 5, 25),
    schedule_interval='@daily'
)

# Define the tasks
artists = PythonOperator(task_id='get_artists', python_callable=get_artists, dag=dag)
albums = PythonOperator(task_id='get_albums', python_callable=get_albums, dag=dag)
songs = PythonOperator(task_id='get_songs', python_callable=get_songs, dag=dag)

# Define the task dependencies
artists >> albums >> songs