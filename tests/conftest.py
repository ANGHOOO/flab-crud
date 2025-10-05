from sqlalchemy import create_engine
from fastapi.testclient import TestClient
from pytest import fixture
from sqlalchemy.orm import sessionmaker

from app.database import Base, get_db
from app.main import app

DATABASE_URL = "sqlite:///test.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@fixture(scope="function")
def client() -> TestClient:
    return TestClient(app)

@fixture(scope="function")
def db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@fixture(scope="function")
def db_client(db):
    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    test_client = TestClient(app)
    yield test_client
    app.dependency_overrides.clear()
    return test_client

