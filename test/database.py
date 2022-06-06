# every thing moved to conftest.py
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.database import get_db,Base
from app.main_sqlalchemy import app

from app.config import settings
from alembic import command

#SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:EdgePower2005+@localhost:5432/fastapi_test'
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

#@pytest.fixture(scope="module")
@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine) 
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

#@pytest.fixture(scope="module")
@pytest.fixture()
def client(session):
    #run our code before we run our test
    #Base.metadata.drop_all(bind=engine) 
    #Base.metadata.create_all(bind=engine)
    #command.upgrade("head")
    def override_get_db():

        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app=app)
    #command.downgrade("base")
    #run our code after our test finishes