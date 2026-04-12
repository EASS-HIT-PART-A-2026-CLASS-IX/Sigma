"""Pytest configuration and fixtures for the Math Teaching API."""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from math_app.app.main import app
from math_app.core.database import get_session
from math_app.core.models_orm import Base


# Create an in-memory SQLite database for testing
@pytest.fixture(scope="function")
def test_db():
    """Create a test database using SQLite in-memory."""
    # Use SQLite in-memory database for fast testing
    engine = create_engine("sqlite:///:memory:")
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    # Create session factory
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    yield TestingSessionLocal, engine
    
    # Cleanup
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db_session(test_db):
    """Provide a database session for testing."""
    TestingSessionLocal, engine = test_db
    session = TestingSessionLocal()
    yield session
    session.close()


@pytest.fixture
def client(db_session):
    """Provide a TestClient with database session dependency injection."""
    
    def override_get_session():
        yield db_session
    
    app.dependency_overrides[get_session] = override_get_session
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture
def sample_lesson_create():
    """Sample lesson creation payload."""
    return {
        "title": "Basic Addition",
        "description": "Learn simple addition with single digits",
        "topic": "arithmetic",
        "level": "beginner",
        "problems": [
            {
                "question": "What is 2 + 3?",
                "answer": "5",
                "difficulty": "beginner",
                "hint": "Count on your fingers",
            },
            {
                "question": "What is 5 + 4?",
                "answer": "9",
                "difficulty": "beginner",
                "hint": None,
            },
        ],
    }


@pytest.fixture
def sample_algebra_lesson():
    """Sample algebra lesson creation payload."""
    return {
        "title": "Solving Linear Equations",
        "description": "Solve equations of the form ax + b = c",
        "topic": "algebra",
        "level": "intermediate",
        "problems": [
            {
                "question": "Solve: 2x + 3 = 7",
                "answer": "2",
                "difficulty": "intermediate",
                "hint": "Subtract 3 from both sides",
            }
        ],
    }
