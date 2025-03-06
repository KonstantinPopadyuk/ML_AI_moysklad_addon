# Data API Service

## Overview
Data API Service is a FastAPI-based application designed for efficient data processing and analysis. It provides RESTful endpoints for data manipulation, statistical analysis, and machine learning model integration. Built with scalability and performance in mind, it supports both small-scale deployments and large-scale production environments.

## Features
- **Data Processing**: Clean, transform, and analyze datasets
- **Statistical Analysis**: Compute descriptive statistics and generate visualizations
- **Model Integration**: Serve machine learning models via API endpoints
- **Scalable Architecture**: Designed for horizontal scaling with containerization support
- **Real-time Monitoring**: Integrated with Prometheus and Grafana for performance tracking
- **Authentication**: JWT-based authentication for secure API access
- **Rate Limiting**: Configurable rate limits to prevent abuse
- **Caching**: Redis-backed caching for improved performance

## Installation

### Prerequisites
- Python 3.9+
- pip 20.0+
- PostgreSQL 12+ (or any supported database)
- Redis (optional, for caching)

### Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/data-api-service.git
   cd data-api-service
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up the database:
   ```bash
   alembic upgrade head
   ```


## Running the Application
Start the FastAPI server:
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8005`

## API Documentation
Interactive API documentation is available at:
- Swagger UI: `http://localhost:8005/docs`

## Endpoints

### Authentication
- `POST /auth/token` - Generate JWT token for authentication
- `GET /auth/validate_token` - Validate JWT token

### Data Analysis
- `GET /react_data/agents_type_grid` - Get sales data by company type
- `GET /react_data/agents_name_grid` - Get sales data by agent name
- `GET /react_data/item_type_grid` - Get sales data by product category
- `GET /react_data/volume_type_grid` - Get sales data by product volume
- `GET /react_data/city_grid` - Get sales data by city

### Predictions
- `GET /react_data/preds/stock` - Get stock predictions
- `GET /react_data/preds/stock_days/{n}` - Get stock predictions for N days

### Cache Management
- `DELETE /react_data/cache/clear` - Clear Redis cache

## Deployment
### Docker
Build and run the container:
```bash
docker-compose up --build
```

## Security
- JWT-based authentication
- Rate limiting
- Input validation using Pydantic
- HTTPS support (via reverse proxy)
- Environment variable management with python-dotenv

## Performance Optimization
- Redis caching for frequent queries
- Asynchronous endpoints using FastAPI's async/await
- Database connection pooling
- Gzip compression for large responses

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.