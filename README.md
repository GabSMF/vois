# Vois API Gateway

A database-agnostic API gateway for the Vois capture service, built with FastAPI and dependency injection.

## Overview

This API provides a clean, implementation-independent interface for managing multimedia captures. The gateway is designed to be:

- **Database Agnostic**: No direct database dependencies - uses abstract interfaces
- **Worker Agnostic**: No direct worker dependencies - uses abstract processing services
- **Testable**: In-memory implementations provided for development/testing
- **Extensible**: Easy to swap implementations via dependency injection

## Architecture

```
app/
├── domain/
│   ├── models.py          # Core business entities (dataclasses)
│   ├── interfaces.py      # Abstract contracts for repositories/services
│   └── container.py       # Dependency injection container
├── infrastructure/
│   └── implementations.py # Concrete implementations (in-memory for dev)
├── config/
│   └── di_config.py       # Dependency injection configuration
├── api/
│   ├── dto.py            # Request/Response DTOs
│   ├── captures.py       # Capture management endpoints
│   └── search.py         # Search endpoints
└── main.py               # FastAPI application entry point
```

## Quick Start

### Installation

```bash
pip install -r requirements.txt
```

### Running the API

```bash
# Development mode with auto-reload
uvicorn app.main:app --reload

# Production mode
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

### API Documentation

Once running, visit `http://localhost:8000/docs` for interactive Swagger documentation.

## API Endpoints

### Captures

#### Create Capture
```http
POST /captures/
Content-Type: application/json

{
  "title": "My Capture",
  "description": "Optional description"
}
```

#### Upload Audio
```http
POST /captures/{capture_id}/audio
Content-Type: multipart/form-data

file: [audio file]
```

#### Upload Image
```http
POST /captures/{capture_id}/images
Content-Type: multipart/form-data

file: [image file]
```

#### Get Status
```http
GET /captures/{capture_id}/status
```

#### Get Timeline
```http
GET /captures/{capture_id}/timeline
```

#### Process Capture
```http
POST /captures/{capture_id}/process
```

#### Delete Capture
```http
DELETE /captures/{capture_id}
```

### Search

#### Global Search
```http
POST /search/global
Content-Type: application/json

{
  "query": "search term",
  "limit": 10,
  "offset": 0
}
```

#### Capture-Specific Search
```http
POST /search/captures/{capture_id}
Content-Type: application/json

{
  "query": "search term",
  "limit": 10
}
```

## Dependency Injection

The API uses a clean dependency injection pattern:

1. **Abstract Interfaces** define contracts in `domain/interfaces.py`
2. **Concrete Implementations** in `infrastructure/implementations.py`
3. **Container Configuration** in `config/di_config.py`
4. **API Endpoints** use `Depends()` to inject services

### Adding New Implementations

To add production implementations (e.g., SQLAlchemy repositories, Celery workers):

1. Create concrete classes implementing the abstract interfaces
2. Register them in `config/di_config.py`
3. The API endpoints will automatically use the new implementations

Example:
```python
# In implementations.py
class SQLAlchemyCaptureRepository(CaptureRepository):
    def __init__(self, session_factory):
        self.session_factory = session_factory
    
    async def create(self, title: str, description: Optional[str] = None) -> Capture:
        # SQLAlchemy implementation
        pass

# In di_config.py
def configure_production_container():
    # Register production implementations
    register_service("capture_repository", SQLAlchemyCaptureRepository(session_factory))
    # ... other services
```

## Development

### Running Tests

```bash
# The in-memory implementations make testing easy
python -m pytest
```

### Code Structure

- **Domain Layer**: Pure business logic, no infrastructure dependencies
- **Infrastructure Layer**: Concrete implementations of domain interfaces
- **API Layer**: HTTP endpoints using dependency injection
- **Configuration Layer**: Dependency injection setup

### Key Principles

1. **Dependency Inversion**: High-level modules don't depend on low-level modules
2. **Single Responsibility**: Each class has one reason to change
3. **Open/Closed**: Open for extension, closed for modification
4. **Interface Segregation**: Clients depend only on methods they use

## Production Deployment

For production:

1. Replace in-memory implementations with production ones
2. Add proper logging and monitoring
3. Configure database connections
4. Set up worker queues (Celery, etc.)
5. Add authentication/authorization
6. Configure CORS, rate limiting, etc.

The API gateway design makes these changes straightforward - just swap implementations in the DI container.