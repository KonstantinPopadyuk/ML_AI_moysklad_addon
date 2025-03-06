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
    'data_retrieval_pipeline',
    default_args=default_args,
    description='Pipeline for creating up-to-date data in DB from MoySkald (by using DataRetriveService API)',
    schedule_interval='@daily',
    catchup=False
)

# Check if the service is available
check_service = HttpSensor(
    task_id='check_service_availability',
    http_conn_id='data_retrieval',
    endpoint='/',
    method='GET',
    response_check=lambda response: response.status_code == 200,
    dag=dag
)

# Create agents data
create_agents = HttpOperator(
    task_id='create_agents',
    http_conn_id='data_retrieval',
    endpoint='/agents/create',
    method='POST',
    dag=dag
)

# Create assortment data
create_assortment = HttpOperator(
    task_id='create_assortment',
    http_conn_id='data_retrieval',
    endpoint='/assortment/create',
    method='POST',
    dag=dag
)

# Create sales data
create_sales = HttpOperator(
    task_id='create_sales',
    http_conn_id='data_retrieval',
    endpoint='/sales/create',
    method='POST',
    dag=dag
)

# Create stock data
create_stock = HttpOperator(
    task_id='create_stock',
    http_conn_id='data_retrieval',
    endpoint='/stock/create',
    method='POST',
    dag=dag
)

# delete agents data
delete_agents = HttpOperator(
    task_id='delete_agents',
    http_conn_id='data_retrieval',
    endpoint='/agents/delete',
    method='DELETE',
    dag=dag
)

# delete assortment data
delete_assortment = HttpOperator(
    task_id='delete_assortment',
    http_conn_id='data_retrieval',
    endpoint='/assortment/delete',
    method='DELETE',
    dag=dag
)

# delete sales data
delete_sales = HttpOperator(
    task_id='delete_sales',
    http_conn_id='data_retrieval',
    endpoint='/sales/delete',
    method='DELETE',
    dag=dag
)

# delete stock data
delete_stock = HttpOperator(
    task_id='delete_stock',
    http_conn_id='data_retrieval',
    endpoint='/stock/delete',
    method='DELETE',
    dag=dag
)


# Check if the service is available
check_service_after_deletion = HttpSensor(
    task_id='check_service_availability_after_deletion',
    http_conn_id='data_retrieval',
    endpoint='/',
    method='GET',
    response_check=lambda response: response.status_code == 200,
    dag=dag
)

# Define task dependencies
clear_all_tasks = [delete_assortment, delete_stock, delete_agents, delete_sales]
check_service >> clear_all_tasks >> check_service_after_deletion >> [create_assortment, create_stock, create_agents] >> create_sales 