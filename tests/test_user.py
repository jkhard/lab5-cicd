from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)

# Существующие пользователи
users = [
    {
        'id': 1,
        'name': 'Ivan Ivanov',
        'email': 'i.i.ivanov@mail.com',
    },
    {
        'id': 2,
        'name': 'Petr Petrov',
        'email': 'p.p.petrov@mail.com',
    }
]

def test_get_existed_user():
    '''Получение существующего пользователя'''
    response = client.get("/api/v1/user", params={'email': users[0]['email']})
    assert response.status_code == 200
    assert response.json() == users[0]

def test_get_unexisted_user():
    '''Получение несуществующего пользователя'''
    response = client.get("/api/v1/user", params={'email': 'notexist@mail.com'})
    assert response.status_code == 404    
    assert "detail" in response.json()

def test_create_user_with_valid_email():
    '''Создание пользователя с уникальной почтой'''
    new_user = {
        'name': 'Ivan Sidorov',
        'email': 'i.sidor@mail.com'
    }
    response = client.post("/api/v1/user", json=new_user)
    assert response.status_code == 201    
    created_user = response.json()
    
    assert created_user['name'] == new_user['name']
    assert created_user['email'] == new_user['email']
    assert 'id' in created_user

def test_create_user_with_invalid_email():
    duplicate_user = {
        'name': 'Duplicate Name',
        'email': users[0]['email']  
    }
    
    response = client.post("/api/v1/user", json=duplicate_user)
    
    assert response.status_code == 409
    assert "detail" in response.json()

def test_delete_user():
    '''Удаление пользователя'''
    new_user = {
        'name': 'User To Delete',
        'email': 'todelete@mail.com'
    }
    
    create_response = client.post("/api/v1/user", json=new_user)
    assert create_response.status_code == 201
    
    user_id = create_response.json()['id']
    
    delete_response = client.delete(f"/api/v1/user/{user_id}")

    assert delete_response.status_code == 200
    assert "message" in delete_response.json()
    get_response = client.get("/api/v1/user", params={'email': new_user['email']})
    assert get_response.status_code == 404