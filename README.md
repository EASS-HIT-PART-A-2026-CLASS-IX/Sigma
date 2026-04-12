# Math Teaching API – EX1 Backend

A simplified FastAPI backend for teaching mathematics progressively, from basic arithmetic through algebra and geometry. This project demonstrates core backend patterns: CRUD operations, data validation, error handling, and comprehensive testing.

---

## Overview

**Theme:** Math Teaching System  
**Core Resource:** Lessons (each containing one or more math problems)  
**Persistence:** MySQL with SQLAlchemy ORM (Alembic migrations)  
**User Progress:** Lesson-level tracking (prepared for authentication)  
**Testing:** pytest + FastAPI TestClient  

### Key Features

- ✅ Full CRUD operations on lessons and problems
- ✅ Topic-based organization (arithmetic, algebra, geometry)
- ✅ Difficulty levels (beginner, intermediate, advanced)
- ✅ Data validation with Pydantic
- ✅ Custom error handling and HTTP exceptions
- ✅ MySQL database with SQLAlchemy ORM
- ✅ Database migrations with Alembic
- ✅ User progress tracking (session-ready for authentication)
- ✅ 25+ comprehensive pytest test cases (80%+ coverage)
- ✅ RESTful API with OpenAPI/Swagger documentation
- ✅ Sample data auto-seeded on startup
- ✅ Docker + Docker Compose for containerized deployment
- ✅ REST Client `.http` playground

---

## Project Structure

```
ex1_math/
├── math_app/
│   ├── __init__.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── models.py              # Pydantic schemas (Lesson, Problem, etc.)
│   │   ├── models_orm.py          # SQLAlchemy ORM models (LessonORM, UserORM, etc.)
│   │   ├── database.py            # Database configuration and session management
│   │   ├── repository.py          # Legacy in-memory storage (deprecated)
│   │   └── exceptions.py          # Custom exception classes
│   ├── app/
│   │   ├── __init__.py
│   │   └── main.py                # FastAPI app and endpoints
│   ├── scripts/
│   │   ├── __init__.py
│   │   └── init_db.py             # Database initialization and seeding script
│   └── tests/
│       ├── __init__.py
│       ├── conftest.py            # pytest fixtures and setup
│       └── test_lessons.py        # Test cases (CRUD, validation, errors)
├── alembic/
│   ├── __init__.py
│   ├── env.py                     # Alembic migration environment
│   ├── script.py.mako             # Migration template
│   └── versions/
│       ├── __init__.py
│       └── 001_initial_schema.py  # Initial schema creation
├── docs/
│   └── lessons.http               # REST Client requests
├── sample_db.json                 # Sample data (auto-seeded on startup)
├── .env                           # Environment variables (DATABASE_URL, etc.)
├── alembic.ini                    # Alembic configuration
├── pyproject.toml                 # Project metadata and dependencies
├── Dockerfile                     # Docker container definition
├── docker-compose.yml             # Docker Compose orchestration
├── .dockerignore                  # Files to exclude from Docker build
├── README.md                      # This file
└── .gitignore                     # Git ignore rules
```


---

## Setup & Installation

### Prerequisites
- Python 3.11 or later
- MySQL 8.0+ (or use Docker Compose for containerized MySQL)
- pip and venv (built-in with Python)

### Step 1: Clone the Repository
```bash
cd ex1_math
```

### Step 2: Create Virtual Environment and Install Dependencies
```bash
# Create virtual environment
python -m venv .venv

# Activate the virtual environment
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -e .
```

### Step 3: Set Up Database

#### Option A: Using Docker Compose (Recommended)
```bash
# Start MySQL and FastAPI with Docker Compose
docker-compose up
# The database will be automatically initialized and populated with sample data
```

#### Option B: Local MySQL Setup
```bash
# 1. Ensure MySQL is running locally
# 2. Create the database
mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS math_app;"

# 3. Initialize the database (creates tables and seeds sample data)
python math_app/scripts/init_db.py
```

### Step 4: Verify Installation
```bash
python -c "import fastapi; print('FastAPI installed:', fastapi.__version__)"
```

---

## Running the API

### Option 1: Docker Compose (Recommended - Full Stack)

#### Start with Docker Compose
```bash
# Build and start both MySQL and FastAPI
docker-compose up

# Or run in the background
docker-compose up -d

# View logs
docker-compose logs -f api
```

The API will be available at:
- **Base URL**: `http://localhost:8000`
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **MySQL**: `localhost:3306` (user: `root`, password: `rootpassword`)

**Database Initialization:**
- Alembic migrations run automatically on container startup
- Sample data from `sample_db.json` is seeded if the database is empty
- Persistent volume `mysql_data` stores database files

#### Stop Docker Compose
```bash
# Stop and remove containers
docker-compose down

# Stop and remove containers + volumes (wipes database)
docker-compose down -v
```

---

### Option 2: Local Development (Manual MySQL)

#### Prerequisites
- MySQL running locally (e.g., via `docker run -p 3306:3306 -e MYSQL_ROOT_PASSWORD=rootpassword mysql:8.0`)
- Database created: `CREATE DATABASE math_app;`
- `.env` file configured with `DATABASE_URL`

#### Start the Development Server
```bash
# Activate virtual environment first
source .venv/bin/activate  # macOS/Linux
# or
.venv\Scripts\activate     # Windows

# Run the FastAPI server
uvicorn math_app.app.main:app --reload
```

The API will be available at:
- **Base URL**: `http://localhost:8000`
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

**Auto-reload enabled**: Changes to Python files automatically restart the server.

---

### Option 3: Docker (without Compose)

#### Build Docker Image Manually
```bash
# Build the image
docker build -t math-teaching-api:latest .
```

#### Run the Container
```bash
# Run standalone (you must have MySQL running separately)
docker run -p 8000:8000 \
  -e DATABASE_URL=mysql+pymysql://root:rootpassword@host.docker.internal:3306/math_app \
  math-teaching-api:latest
```

#### Notes
- The container will attempt to initialize the database on startup
- Using `host.docker.internal` allows the container to access MySQL on the host machine

---


### Example API Requests

#### 1. Health Check
```bash
curl http://localhost:8000/health
```

#### 2. Create a Lesson
```bash
curl -X POST http://localhost:8000/lessons \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Basic Addition",
    "description": "Learn simple addition with single digits",
    "topic": "arithmetic",
    "level": "beginner",
    "problems": [
      {
        "question": "What is 2 + 3?",
        "answer": "5",
        "difficulty": "beginner",
        "hint": "Count on your fingers"
      }
    ]
  }'
```

#### 3. List All Lessons
```bash
curl http://localhost:8000/lessons
```

#### 4. List Lessons by Topic
```bash
curl "http://localhost:8000/lessons?topic=arithmetic"
```

#### 5. Get a Specific Lesson
```bash
curl http://localhost:8000/lessons/{lesson_id}
```

#### 6. Update a Lesson
```bash
curl -X PUT http://localhost:8000/lessons/{lesson_id} \
  -H "Content-Type: application/json" \
  -d '{"title": "Advanced Addition"}'
```

#### 7. Delete a Lesson
```bash
curl -X DELETE http://localhost:8000/lessons/{lesson_id}
```

---

## Running Tests

### Run All Tests
```bash
# Using uv:
uv run pytest

# Or with activated venv:
pytest
```

### Run Tests with Coverage Report
```bash
uv run pytest --cov=math_app --cov-report=html
```

### Run Specific Test File
```bash
uv run pytest math_app/tests/test_lessons.py -v
```

### Run Specific Test Class
```bash
uv run pytest math_app/tests/test_lessons.py::TestCreateLesson -v
```

### Run Specific Test Function
```bash
uv run pytest math_app/tests/test_lessons.py::TestCreateLesson::test_create_lesson_minimal -v
```

### Test Results
Expected output:
```
collected 25 items

math_app/tests/test_lessons.py::TestHealth::test_health_check_returns_healthy PASSED
math_app/tests/test_lessons.py::TestCreateLesson::test_create_lesson_minimal PASSED
math_app/tests/test_lessons.py::TestCreateLesson::test_create_lesson_with_problems PASSED
...
========================= 25 passed in 1.23s =========================
```

---

## Bonus Features

### 1. Sample Database (sample_db.json)
The project includes a lightweight `sample_db.json` file that provides starter data:

- Automatically loaded when the API starts
- Contains 2 sample lessons for testing
- Easy to modify with additional lessons
- Located at the project root

To add more sample lessons, edit `sample_db.json`:
```json
{
  "lessons": [
    {
      "id": "lesson-003",
      "title": "Your Lesson Title",
      "description": "Your lesson description",
      "topic": "arithmetic",
      "level": "beginner",
      "problems": [...],
      "created_at": "2024-01-15T10:40:00"
    }
  ]
}
```

After modifying, restart the API to reload the changes.

### 2. REST Client Playground
Use the `.http` file with VS Code REST Client extension or Postman:

```bash
# View the file:
code docs/lessons.http
```

The file contains pre-configured requests for all CRUD operations. Hit the arrow button next to each request to execute directly from the editor.

---

## API Endpoints Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/health` | Health check |
| `POST` | `/lessons` | Create a new lesson |
| `GET` | `/lessons` | List all lessons (with optional filtering) |
| `GET` | `/lessons/{id}` | Get a specific lesson |
| `PUT` | `/lessons/{id}` | Update a lesson |
| `DELETE` | `/lessons/{id}` | Delete a lesson |

### Query Parameters

- **`topic`** (optional): Filter by topic (`arithmetic`, `algebra`, `geometry`)
- **`level`** (optional): Filter by level (`beginner`, `intermediate`, `advanced`)

### Response Status Codes

| Code | Meaning |
|------|---------|
| `200` | Success (GET, PUT) |
| `201` | Created (POST) |
| `204` | No Content (DELETE) |
| `404` | Not Found |
| `422` | Validation Error |

---

## Data Models

### Lesson
```json
{
  "id": "string (UUID)",
  "title": "string",
  "description": "string",
  "topic": "arithmetic | algebra | geometry",
  "level": "beginner | intermediate | advanced",
  "problems": [
    {
      "id": "string (UUID)",
      "question": "string",
      "answer": "string",
      "difficulty": "beginner | intermediate | advanced",
      "hint": "string (optional)"
    }
  ],
  "created_at": "ISO 8601 datetime"
}
```

### Topic Enum
- `arithmetic`
- `algebra`
- `geometry`

### Level Enum
- `beginner`
- `intermediate`
- `advanced`

---

## Architecture

### Layers

1. **Models** (`models.py`): Pydantic schemas for request/response validation
2. **Repository** (`repository.py`): In-memory data layer with CRUD operations
3. **Exceptions** (`exceptions.py`): Custom exceptions with HTTP status mapping
4. **API** (`app/main.py`): FastAPI endpoints with dependency injection

### Design Patterns

- **Repository Pattern**: Abstraction for data persistence (easy migration to DB)
- **Dependency Injection**: FastAPI `Depends()` for testability
- **Pydantic Validation**: Type checking and schema validation
- **Custom Exceptions**: Decoupled error handling

---

## Testing Strategy

### Test Coverage
- **25+ test cases** across 6 test classes
- **Happy path workflows**: Create → Read → Update → Delete
- **Edge cases**: Empty data, missing IDs, invalid inputs
- **Error handling**: 404 Not Found, 422 Validation errors
- **Filtering**: By topic and level

### Test Files
- `conftest.py`: Fixtures (TestClient, sample data)
- `test_lessons.py`: Main test suite with 6 test classes

### Running Tests Locally
After setting up the environment:
```bash
uv run pytest math_app/tests/ -v --tb=short
```

---

## Troubleshooting

### Docker Issues

#### Container won't start
```bash
# Check logs for errors
docker-compose logs api

# Rebuild the image
docker-compose build --no-cache
docker-compose up
```

#### Port 8000 already in use (Docker)
```bash
# Modify docker-compose.yml to use a different port:
# Change "8000:8000" to "8001:8000"
# Then restart
docker-compose down
docker-compose up
```

#### Clear Docker resources
```bash
# Stop all containers
docker-compose down

# Remove the container and image
docker remove math_teaching_api
docker image rm math-teaching-api:latest
```

---

### Port Already in Use
If port 8000 is already in use:
```bash
uvicorn math_app.app.main:app --reload --port 8001
```

### Import Errors
Ensure the virtual environment is activated:
```bash
# Windows:
.venv\Scripts\activate

# macOS/Linux:
source .venv/bin/activate
```

### Tests Fail
Check that pytest and httpx are installed:
```bash
uv sync
# or
pip install pytest httpx
```

### Dependency Issues
Clear the cache and reinstall:
```bash
rm uv.lock
uv sync
```

---

## References

- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Pydantic Docs](https://docs.pydantic.dev/)
- [pytest Documentation](https://docs.pytest.org/)
- [REST API Best Practices](https://restfulapi.net/)

---

## License

This project is part of the EASS-HIT course (Exercise 1) and is provided as-is for educational purposes.

---

**Version**: 0.1.0  
**Last Updated**: April 2026  
**Author**: Student
