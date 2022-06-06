# pytest -v -s test\test_users.py -x
from app import schemas
from app.config import settings 
from jose import jwt
import pytest

def test_create_user(client,session):
    res = client.post("/users/",json={"email":"hello123@gmail.com","password":"password123"})
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "hello123@gmail.com"
    assert res.status_code == 201

def test_login_user(test_user,client):
    res = client.post("/login",data={"username":test_user['email'],"password":test_user['password']})
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token,settings.secret_key,algorithms=[settings.algorithm])
    id = payload.get("user_id")
    #print (res.json())
    assert res.status_code == 200
    assert id == test_user['id']
    assert login_res.token_type == "bearer"

@pytest.mark.parametrize("email,password,status_code",[
    ('wrongemail@gmail.com','123456',403),
    ('testuser@gmail.com','wrongpassword',403),
    ('wrongemail@gmail.com','wrongpassword',403),
    (None,'123456',422),
    ('testuser@gmail.com',None,422),
])
def test_incorrect_login(test_user,client,email,password,status_code):
    res = client.post("/login",data={"username":email,"password":password})

    assert res.status_code == status_code
    
