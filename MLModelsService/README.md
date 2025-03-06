# ML Models Service

This is a FastAPI-based service that provides machine learning models and analytics for sales predictions and reports. The service includes various endpoints for generating reports, making predictions, and updating models.

## Features

- **Sales and Stock Predictions**: Generate predictions for stock needs and sales trends.
- **Recommendation models**: Generate predictions for similar goods.
- **Reports**: Generate various reports based on sales data, including agent types, item types, volumes, and city data.
- **Model Management**: Update and manage machine learning models for sales predictions.

## Getting Started

### Prerequisites

- Python 3.12
- Docker (optional, for containerized deployment)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/MLModelsService.git
   cd MLModelsService
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up Redis (required for caching):
   ```bash
   docker run -d --name redis -p 6379:6379 redis
   ```

### Running the Service

To run the service locally:
```bash
uvicorn main:app --host 0.0.0.0 --port 8010
```

Alternatively, you can use Docker to run the service:
```bash
docker build -t mlmodelservice .
docker run -d --name mlmodelservice -p 8010:8010 mlmodelservice
```

### API Endpoints

#### Reports
- **GET /get_agents_type_report**: Get a report on agent types.
- **GET /get_agents_name_data**: Get a report on agent names.
- **GET /get_item_type_data**: Get a report on item types.
- **GET /get_volumes_data**: Get a report on volumes.
- **GET /get_city_data**: Get a report on city data.

#### Predictions
- **GET /create_stock_preds**: Generate stock predictions.
- **GET /create_stock_preds?n=30**: Generate stock predictions for the next `n` days.

#### Model Management
- **GET /multi_goods_7_30-60**: Update the multi-goods 7-30-60 model.

### Configuration

The service uses Redis for caching. Ensure that Redis is running and accessible at `redis:6379`. You can modify the Redis connection settings in `routers/rediscachewrapper.py`.