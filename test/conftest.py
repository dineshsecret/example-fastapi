#all fixures goes here
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.database import get_db,Base
from app.main_sqlalchemy import app
from app.oauth2 import create_access_token
from app.config import settings
from alembic import command
from app import schemas,models
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

@pytest.fixture
def test_user2(client):
    user_data = {
        "email":"testuser1@gmail.com",
        "password":"123456"
    }

    res = client.post("/users/",json=user_data)
    new_user = schemas.UserOut(**res.json())
    assert res.status_code == 201
    assert new_user.email == user_data['email']
    new_user = res.json()
    new_user['password'] = user_data["password"]

    return new_user

@pytest.fixture
def test_user(client):
    user_data = {
        "email":"testuser@gmail.com",
        "password":"123456"
    }

    res = client.post("/users/",json=user_data)
    new_user = schemas.UserOut(**res.json())
    assert res.status_code == 201
    assert new_user.email == user_data['email']
    new_user = res.json()
    new_user['password'] = user_data["password"]

    return new_user

@pytest.fixture
def token(test_user):
    return create_access_token({"user_id":test_user['id']})

@pytest.fixture
def authorized_client(client,token):
    print ('im in authorized client')
    client.headers = {
        **client.headers,
        "Authorization":f"Bearer {token}"
    }

    return client

@pytest.fixture
def test_post(test_user,session,test_user2):
    posts_data = [
        {"title":"1st title",
        "content":"1st content",
        "owner_id":test_user['id']},
        {"title":"2nd title",
        "content":"2nd content",
        "owner_id":test_user['id']},
        {"title":"3rd title",
        "content":"3td content",
        "owner_id":test_user['id']},
        {"title":"4th title",
        "content":"4th content",
        "owner_id":test_user2['id']}
    ]

    def create_post_model(post):
        return models.Post(**post)

    post_map = map(create_post_model,posts_data)
    posts = list(post_map)
    session.add_all(posts)
    # session.add_all([models.Post(title="1st title",content="1st content",owner_id=test_user['id']),
    # models.Post(title="2st title",content="2nd content",owner_id=test_user['id']),
    # models.Post(title="3rd title",content="3rd content",owner_id=test_user['id'])])

    session.commit()

    posts = session.query(models.Post).all()
    
    return posts
