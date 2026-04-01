# Price Monitoring System

## Overview

This project implements a production-style price monitoring platform that ingests product data from multiple marketplaces (1stdibs, Grailed, Fashionphile), tracks price changes over time, exposes analytics APIs, and provides a dashboard for visualization.

The system is designed with extensibility, reliability, and scalability in mind.

Core capabilities:

* Multi-source ingestion pipeline
* Historical price tracking
* Analytics endpoints
* Secure API access with usage tracking
* Webhook-based price change notifications
* Interactive dashboard with charts

## Architecture

The system follows a layered service architecture:

```
Marketplace JSON Sources
        ↓
Ingestion Service
        ↓
PostgreSQL Database
        ↓
Analytics + API Layer (FastAPI)
        ↓
React Dashboard
```

Main components:

| Layer         | Responsibility                        |
| ------------- | ------------------------------------- |
| Ingestion     | Normalizes marketplace snapshots      |
| Database      | Stores product state + price history  |
| API           | Query, refresh, analytics endpoints   |
| Notifications | Persistent webhook delivery queue     |
| Auth          | API-key validation + request tracking |
| Frontend      | Dashboard visualization               |

## Setup Instructions

### 1. Clone repository

```
git clone <repo-url>
cd price-monitoring-system
```

### 2. Create virtual environment

```
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```
pip install -r requirements.txt
```

### 4. Configure environment variables

Create `.env` file:

```
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/price_monitor
DEFAULT_API_KEY=test-key-123
```

### 5. Initialize database

```
python scripts/init_db.py
```

### 6. Run ingestion

```
python -m scripts.run_ingestion
```

### 7. Start backend server

```
uvicorn app.main:app --reload
```

### 8. Start dashboard

```
cd dashboard
npm install
npm start
```

## API Documentation

Swagger UI available at:

```
http://127.0.0.1:8000/docs
```

Main endpoints:

| Endpoint                     | Description                 |
| ---------------------------- | --------------------------- |
| POST /refresh                | Trigger ingestion refresh   |
| GET /products                | Browse products             |
| GET /products/{id}           | Product details             |
| GET /products/{id}/history   | Price history               |
| GET /analytics/summary       | Aggregate statistics        |
| POST /notifications/dispatch | Send pending webhook events |

## Authentication

All API requests require header:

```
x-api-key: test-key-123
```

Requests are logged for usage tracking.

## Notification System

Price changes generate persistent notification events stored in the database.

A dispatcher service:

* retrieves pending events
* sends webhook payloads
* retries failed deliveries
* tracks retry attempts

This guarantees delivery reliability without blocking ingestion.

## Scaling Strategy

### Handling millions of price history rows

The system separates:

```
products (latest snapshot)
price_history (time-series data)
```

Future scaling improvements:

* partition price_history by time
* add index on product_id
* introduce materialized analytics views
* move cold data to archival storage

### Supporting 100+ marketplaces

Marketplace ingestion uses a source detection layer:

```
filename → adapter → normalized schema
```

Future extension:

* adapter registry pattern
* plugin ingestion modules
* async ingestion workers

### Improving webhook reliability

Notification events are persisted before delivery.

Future improvements:

* exponential backoff retries
* dead-letter queue
* background worker scheduler
* distributed task queue (Celery / Redis)

## Testing

Run test suite:

```
pytest
```

Includes tests for:

* refresh pipeline
* product queries
* analytics endpoint
* history tracking
* authentication enforcement
* usage logging

## Limitations

Current implementation assumes:

* snapshot-based ingestion input
* synchronous webhook dispatch endpoint
* single-node deployment

## Future Improvements

Potential enhancements:

* async ingestion scheduler
* streaming updates
* rate limiting middleware
* caching analytics responses
* distributed ingestion workers

## Design Decisions

### PostgreSQL over SQLite

Chosen for:

* time-series scalability
* indexing support
* production-readiness

### FastAPI over Flask/Django

Chosen for:

* async support
* automatic OpenAPI docs
* performance
* type-safe request validation

### Some Screenshots
![Dynamic Graph denoting history of a product](image.png)

![Dashboard](image-1.png)

![SwaggerUI to test the backend APIs](image-2.png)

![Analytics_dashboard](image-3.png)

### Event-driven notifications

Webhook delivery uses a persistent event table to ensure failures do not block ingestion and events are never lost.

## Author

Krishan - BE CSE, Chitkara University
