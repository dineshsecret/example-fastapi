
from typing import List

import pytest
from sqlalchemy import true
from app import schemas
from test.conftest import client

def test_get_all_post(authorized_client,test_post):
    res = authorized_client.get("/posts/")

    def validate(post):
        return schemas.PostOut(**post)

    post_map = map(validate,res.json())
    posts_list = list(post_map)
    print(list(post_map))

    assert len(res.json()) == len(test_post)
    assert res.status_code == 200
    

def test_unauthorized_user_get_one_posts(client,test_post):
    res = client.get(f"/posts/{test_post[0].id}")
    assert res.status_code == 401

def test_unauthorized_user_get_all_posts(client,test_post):
    res = client.get("/posts/")
    assert res.status_code == 401

def test_get_one_post_not_exist(authorized_client,test_post):
    res = authorized_client.get(f"/posts/8888")
    assert res.status_code == 404

def test_get_one_post(authorized_client,test_post):
    res = authorized_client.get(f"/posts/{test_post[0].id}")
    
    post = schemas.PostOut(**res.json())
    
    assert post.Post.id == test_post[0].id
    assert post.Post.content == test_post[0].content

@pytest.mark.parametrize("title,content,published",[
    ("aaaaa","awsome1",True),
    ("bbbbb","awsome2",False),
    ("ccccc","awsome3",True),
    ("ddddd","awsome4",False),
])

def test_create_post(authorized_client, test_user,test_post,title,content,published):
    res = authorized_client.post("/posts/",json={"title":title,"content":content,"published":published})

    created_post = schemas.Post(**res.json())
    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content ==  content
    assert created_post.published == published
    assert created_post.owner_id == test_user['id']

def test_create_posts_default_published_true(authorized_client, test_user,test_post):
    res = authorized_client.post("/posts/",json={"title":"arbitrary title","content":"dsfdsfsdf"})

    created_post = schemas.Post(**res.json())
    assert res.status_code == 201
    assert created_post.title == "arbitrary title"
    assert created_post.content ==  "dsfdsfsdf"
    assert created_post.published == True
    assert created_post.owner_id == test_user['id']

def test_unauthorized_user_create_post(client,test_post):
    res = client.get("/posts/",json={"title":"arbitrary title","content":"dsfdsfsdf"})
    assert res.status_code == 401

def test_unauthorized_user_delete_post(client,test_post):
    res = client.delete(f"/posts/{test_post[0].id}")
    assert res.status_code == 401

def test_authorized_user_delete_post(authorized_client,test_post):
    res = authorized_client.delete(f"/posts/{test_post[0].id}")
    assert res.status_code == 204

def test_delete_post_non_exists(authorized_client,test_post):
    res = authorized_client.delete(f"/posts/8888")
    assert res.status_code == 404

def test_delete_other_user_post(authorized_client,test_user,test_user2,test_post):
    res = authorized_client.delete(f"/posts/{test_post[3].id}")
    assert res.status_code == 403

def test_update_post(authorized_client,test_user,test_post):
    data = {
        "title":"updated title",
        "content":"updated content",
        "id":test_post[0].id
    }

    res = authorized_client.put(f"/posts/{test_post[0].id}",json=data)
    updated_posts = schemas.Post(**res.json())
    assert res.status_code == 200
    assert updated_posts.title == data['title']
    assert updated_posts.content == data['content']

def test_update_other_user_posts(authorized_client,test_user,test_user2,test_post):
    data = {
        "title":"updated title",
        "content":"updated content",
        "id":test_post[3].id
    }

    res = authorized_client.put(f"/posts/{test_post[3].id}",json=data)
    assert res.status_code ==403

def test_unauthorized_user_update_post(client,test_post):
    data = {
        "title":"updated title",
        "content":"updated content",
        "id":test_post[3].id
    }
    res = client.put(f"/posts/{test_post[0].id}")
    assert res.status_code == 401

def test_update_post_non_exists(authorized_client,test_post):
    data = {
        "title":"updated title",
        "content":"updated content",
        "id":test_post[3].id
    }

    res = authorized_client.put(f"/posts/8888",json=data)
    assert res.status_code == 404