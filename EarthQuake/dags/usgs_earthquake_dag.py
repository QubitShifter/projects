from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    "owner": "data",
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}


with DAG(
    dag_id="usgs_earthquake_us_to_bq",
    description="Daily USGS - BigQuery ETL for California earthquakes",
    default_args=default_args,
    start_date=datetime(2018, 5, 1),
    schedule_interval="@daily",   
    catchup=False,                
    max_active_runs=1,
) as dag:

    scrip_path = "/var/opt/airflow/dags/usgs_to_bigquery.py"

    project_id = "earthquake"         
    dataset = "usgs_earthquake"

    run_usgs_etl = BashOperator(
        task_id="run_usgs_etl",
        bash_command=(
            "python {{ params.script_path }} "
            "--project_id={{ params.project_id }} "
            "--dataset={{ params.dataset }} "
            "--start-date={{ ds }} "
            "--end-date={{ ds }} "
            "--min-magnitude=3.0 "
            "--min-latitude=32.0 "
            "--max-latitude=42.0 "
            "--min-longitude=-125.0 "
            "--max-longitude=-114.0 "
            "--page-limit=20000"
        ),
        params={
            "script_path": scrip_path,
            "project_id": project_id,
            "dataset": dataset,
        },
    )
