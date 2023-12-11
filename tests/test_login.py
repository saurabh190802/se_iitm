
def test_login_all_fields_present_and_valid(client):
    login_form_data = {
        "email": "abc@xyz.com",
        "password": "123456"
    }

    response = client.post("/auth/login", data = login_form_data)

    assert response.status_code == 200
    assert response.data == b"""{"email":"abc@xyz.com","first_name":"abc","jwt_token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxfQ.P01EWncYImh8G4Gvp38CYpwVUizWIU9wSK1C5FyrJyo","last_name":"xyz","user_id":1}\n"""


def test_login_some_fields_absent(client):
    incomplete_form_data = {
        "email": "abc@xyz.com"
    }
    response = client.post("/auth/login", data = incomplete_form_data)

    assert response.status_code == 400
    assert response.data == b"""All details have not been sent. Required Fields :
                                           email, password."""
    
def test_login_wrong_email_password(client):
    incorrect_login_data = {
        "email": "abc@xyz.com",
        "password": "abcdef"
    }

    response = client.post("/auth/login", data = incorrect_login_data)

    assert response.status_code == 400
    assert response.data == b'Email or password or both are wrong'
