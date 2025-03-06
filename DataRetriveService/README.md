# Data Retrieve Service

The Data Retrieve Service is a FastAPI-based application designed to fetch and manage data from external APIs (specifically Moysklad) and store it in a PostgreSQL database. The service provides endpoints to retrieve assortment, sales, agents, and stock data, and includes functionality for data transformation and validation.

## Features

- **Data Retrieval**: Fetch data from Moysklad API for assortment, sales, agents, and stock.
- **Data Transformation**: Transform raw API responses into structured data formats suitable for database storage.
- **Database Integration**: Store retrieved data in a PostgreSQL database using SQLAlchemy ORM.
- **API Endpoints**: Expose RESTful API endpoints for accessing the retrieved data.
- **Error Handling**: Implement retry mechanisms and error handling for robust API interactions.
- **CORS Support**: Enable Cross-Origin Resource Sharing (CORS) for frontend integration.

## Technologies

- **Python**: Primary programming language.
- **FastAPI**: Web framework for building the API.
- **SQLAlchemy**: ORM for database interactions.
- **PostgreSQL**: Relational database for data storage.
- **Pandas**: Data manipulation and transformation.
- **Alembic**: Database migration tool.
- **Docker**: Containerization for deployment.

## Getting Started

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-repo/DataRetriveService.git
   cd DataRetriveService
   ```

2. **Set up environment variables**:
   Create a `.env` file in the root directory with the following variables:
   ```env
   DB_USER=postgres
   DB_PASS=postgres
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=postgres
   MOYSKLAD_TOKEN=your_moysklad_token
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run database migrations**:
   ```bash
   alembic upgrade head
   ```

5. **Start the application**:
   ```bash
   uvicorn main:app --reload
   ```

### Docker Setup

1. **Build the Docker image**:
   ```bash
   docker build -t data-retrieve-service .
   ```

2. **Run the Docker container**:
   ```bash
   docker run -p 8000:8000 data-retrieve-service
   ```

## API Endpoints

- **GET /**: Health check endpoint.
- **GET /assortment/**: Retrieve assortment data.
- **GET /sales/**: Retrieve sales data.
- **GET /agents/**: Retrieve agents data.
- **GET /stock/**: Retrieve stock data.

## Data Models

### Assortment
- `position_id`: UUID (Primary Key)
- `id`: String (Unique)
- `updated`: DateTime
- `name`: String
- `description`: String
- `code`: String
- `archived`: Boolean
- `pathname`: String
- `paymentitemtype`: String
- `volume`: Float
- `variantscount`: Float
- `stock`: Float
- `reserve`: Float
- `intransit`: Float
- `quantity`: Float
- `price_usd`: Float
- `price_distr`: Float
- `price_opt`: Float
- `price_proiz`: Float
- `price_rrz`: Float
- `price_site`: Float
- `price_tech`: Float

### Sales
- `id_sale`: UUID (Primary Key)
- `order_id`: String
- `agent_id`: String (Foreign Key)
- `name`: String
- `updated`: DateTime
- `moment`: DateTime
- `created`: DateTime
- `state`: String
- `sum`: Float
- `vatSum`: Float
- `payedSum`: Float
- `shippedSum`: Float
- `invoicedSum`: Float
- `reservedSum`: Float
- `assortment_id`: String (Foreign Key)
- `quantity`: Integer
- `price`: Float
- `shipmentAddress`: String
- `city`: String

### Agents
- `id_agent_base`: UUID (Primary Key)
- `agent_id`: String (Unique)
- `updated`: DateTime
- `name`: String
- `created`: DateTime
- `companyType`: String
- `actualAddress`: String
- `phone`: String
- `tags`: String
- `legalTitle`: String
- `legalLastName`: String
- `legalFirstName`: String
- `email`: String
- `legalAddress`: String

### Stock
- `id_stock_base`: UUID (Primary Key)
- `stock`: Float
- `inTransit`: Float
- `reserve`: Float
- `quantity`: Float
- `name`: String
- `code`: String
- `article`: String
- `stockDays`: Float