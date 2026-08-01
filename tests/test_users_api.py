
# user not exist --- user ok but password is wrong
def test_login_response_401_422(anon_client) :
    payload = {
        'username': "javad" ,
        'password': "Arman#123"
    }
    response = anon_client.post('/users/login', json=payload)
    assert response.status_code == 401
    
    payload = {
        'username': "Arman" ,
        'password': "arman#123"
    }
    response = anon_client.post('/users/login', json=payload)
    assert response.status_code == 422
    


# user and password is ok
def test_login_response_200(anon_client) :
    payload = {
        'username': "test_user" ,
        'password': "Abcd#123"
    }
    response = anon_client.post('/users/login', json=payload)
    assert response.status_code == 200
    assert 'access_token' in response.json()
    assert 'refresh_token' in response.json()