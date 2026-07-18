import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database.base import Base
from app.database.session import get_db
from app.main import app


@pytest.fixture()
def db_session():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    TestingSession = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)
    Base.metadata.create_all(engine)
    session = TestingSession()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(engine)


@pytest.fixture()
def client(db_session):
    def override_db():
        yield db_session

    app.dependency_overrides[get_db] = override_db
    with TestClient(app, raise_server_exceptions=False) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture()
def patient_payload():
    return {
        "first_name": "Jane",
        "last_name": "Doe",
        "date_of_birth": "1990-05-21",
        "sex": "Female",
        "phone_number": "202-555-0147",
        "email": "jane.doe@example.com",
        "address_line_1": "1200 Main Street",
        "address_line_2": "Apt 4B",
        "city": "Washington",
        "state": "dc",
        "zip_code": "20001",
        "preferred_language": "English",
    }
