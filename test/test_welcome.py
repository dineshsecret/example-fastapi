# pytest -v -s test\test_welcome.py -x
from fastapi.testclient import TestClient
from app.main_sqlalchemy import app

client = TestClient(app=app)

def test_root():
    res = client.get("welcome")
    assert res.json().get('message') == 'Welcome to my fastAPI with bind mount'
    assert res.status_code == 200