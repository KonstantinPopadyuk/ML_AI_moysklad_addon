# Airflow Service

This service contains Airflow DAGs that orchestrate data pipelines and machine learning workflows for the project. The service works using a Local Executor to simplify the number of dependencies. To work correctly, you will need to create connections in the admin panel. This may be too powerful a tool for the current functionality, but it is assumed that the number of models and incoming data sources may be significantly larger. Therefore, the current architecture uses AirFlow.

## DAGs Folder Structure

### `data_retrieval_dag.py`
- **Purpose**: Manages the data retrieval and database synchronization pipeline

### `ml_goods_model.py`
- **Purpose**: Handles the creation and updating of stock prediction models
- **Tasks**:
  - Checks service availability
  - Creates/updates multi-goods prediction models (7, 30, 60 days windows)
- **Schedule**: Monthly
- **Dependencies**:
  - `check_service` → `create_stockpreds_model`

## Service Connections

To enable communication between Airflow and other services, you need to create HTTP connections in the Airflow admin panel:

1. **Data Service Connection**
   - **Connection ID**: `data_service_conn`
   - **Connection Type**: HTTP
   - **Host**: `http://data_retrieval:8000`
   - **Description**: Connection to Data Retrieval Service

2. **ML Service Connection**
   - **Connection ID**: `ml_service_conn`
   - **Connection Type**: HTTP
   - **Host**: `http://ml_models:8010`
   - **Description**: Connection to Machine Learning Models Service

### Steps to Create Connections:
1. Access the Airflow Admin Panel
2. Navigate to Admin → Connections
3. Click the "+" button to add a new connection
4. Fill in the connection details as specified above
5. Save the connection