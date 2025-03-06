from airflow import DAG
from airflow.providers.http.operators.http import HttpOperator
from airflow.providers.http.sensors.http import HttpSensor
from datetime import datetime

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2025, 1, 1),
    'retries': 1
}

dag = DAG(
    'create_or_update_goods_model',
    default_args=default_args,
    description='Updating all stock prediction within nearest 7-30-60 days windows (by using MLModelsService API)',
    schedule_interval='@monthly',
    catchup=False
)

check_service = HttpSensor(
    task_id='check_service_availability',
    http_conn_id='ml_models',
    endpoint='/',
    method='GET',
    response_check=lambda response: response.status_code == 200,
    dag=dag
)

create_stockpreds_model = HttpOperator(
    task_id='create_model_multigoods73060',
    http_conn_id='ml_models',
    endpoint='/multi_goods_7_30-60',
    method='GET',
    dag=dag
)

# Define task dependencies
check_service >> create_stockpreds_model