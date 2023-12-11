
def test_signup_all_fields_present_and_valid(client):
    signup_form_data = {
        "first_name" : "test_abc",
        "last_name" : "test_xyz",
        "email" : "test@tester.com",
        "password" : "testing_password"
    }

    response = client.post("/auth/register",data = signup_form_data)

    assert response.status_code == 200
    assert response.data == b'User created'

def test_signup_some_fields_absent(client):
    incomplete_form_data = {
        "first_name" : "test_abc",
        "last_name" : "test_xyz",
        "email" : "test@tester.com",
    }

    response = client.post("/auth/register",data = incomplete_form_data)

    assert response.status_code == 400
    assert response.data == b"""All details have not been sent. Required Fields :
                                           first_name, last_name, email, password."""

def test_signup_with_already_registered_email(client):
    already_existing_user_data = {
        "first_name" : "test_abc",
        "last_name" : "test_xyz",
        "email" : "test@tester.com",
        "password" : "testing_password"
    }

    response = client.post("/auth/register",data = already_existing_user_data)

    assert response.status_code == 400
    assert response.data == b"""User with same email already exists.
                                                 Try with a different email"""
    