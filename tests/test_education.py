from instance.config import TESTING_HEADER, SECOND_USER_TESTING_HEADER

def test_create_education(client):
    education_form_data = {
        'college_name' : 'test_college',
        'joining_year' : 2000,
        'graduation_year' : 2004
    }

    response = client.post('/achievement/education', data = education_form_data,
                           headers = TESTING_HEADER)
    
    assert response.status_code == 200

    assert response.data == b'{"college_name":"test_college","education_id":1,"graduation_year":"2004","joining_year":"2000","user_id":1}\n'


def test_create_education_missing_fields(client):
    missing_education_form_data = {
        'college_name' : 'test_college',
        'joining_year' : 2000
    }

    response = client.post('/achievement/education', data = missing_education_form_data,
                           headers = TESTING_HEADER)
    
    assert response.status_code == 400

    assert response.data ==  b"""All details have not been sent. Required Fields :
                                            college_name, joining_year, graduation_year"""
    

def test_create_education_absent_token(client):
    education_form_data = {
        'college_name' : 'test_college',
        'joining_year' : 2000,
        'graduation_year' : 2004
    }

    response = client.post('/achievement/education', data = education_form_data)

    
    
    assert response.status_code == 400

    assert response.data ==  b'No User Found. Login first.'

def test_create_education_malformed_token(client):
    education_form_data = {
        'college_name' : 'test_college',
        'joining_year' : 2000,
        'graduation_year' : 2004
    }

    response = client.post('/achievement/education', data = education_form_data,
                           headers = {'x-access-token':'abc'})

    
    
    assert response.status_code == 400

    assert response.data ==  b'Malformed Token sent'

def test_get_education_valid_id(client):

    response = client.get('/achievement/education/1', headers = TESTING_HEADER)

    assert response.status_code == 200

    assert response.data == b'{"college_name":"test_college","education_id":1,"graduation_year":2004,"joining_year":2000,"user_id":1}\n'


def test_get_education_invalid_id(client):

    response = client.get('/achievement/education/6', headers = TESTING_HEADER)

    assert response.status_code == 400

    assert response.data == b"Education id doesn't match any existing entry"

def test_get_education_absent_client_token(client):

    response = client.get('/achievement/education/1')

    assert response.status_code == 400

    assert response.data == b'No User Found. Login first.'

def test_update_education_valid(client):
    
    update_education_form_data = {
        'college_name' : 'update_test_college',
        'joining_year' : 2010,
        'graduation_year' : 2014
    }

    response = client.put('/achievement/education/1', data = update_education_form_data,
                          headers = TESTING_HEADER)
    
    assert response.status_code == 200

    assert response.data == b'{"college_name":"update_test_college","education_id":1,"graduation_year":2014,"joining_year":2010,"user_id":1}\n'

def test_update_education_invalid_id(client):

    update_education_form_data = {
        'college_name' : 'update_test_college',
        'joining_year' : 2010,
        'graduation_year' : 2014
    }

    response = client.put('/achievement/education/5', data = update_education_form_data,
                          headers = TESTING_HEADER)
    
    assert response.status_code == 400

    assert response.data == b"Education id doesn't match any existing entry"

def test_update_education_invalid_access(client):

    update_education_form_data = {
        'college_name' : 'update_test_college',
        'joining_year' : 2010,
        'graduation_year' : 2014
    }

    response = client.put('/achievement/education/1', data = update_education_form_data,
                          headers = SECOND_USER_TESTING_HEADER)
    
    assert response.status_code == 400

    assert response.data == b"You don't have permissions to update this entry."


def test_delete_education_invalid_id(client):

    response = client.delete('/achievement/education/5', headers = TESTING_HEADER)

    assert response.status_code == 400

    assert response.data == b"Education id given doesn't match any existing entry"

def test_delete_education_invalid_access(client):

    response = client.delete('/achievement/education/1', headers = SECOND_USER_TESTING_HEADER)

    assert response.status_code == 400

    assert response.data == b"You don't have permissions to delete this entry."

def test_delete_education_valid(client):

    response = client.delete('/achievement/education/1', headers = TESTING_HEADER)

    assert response.status_code == 200

    assert response.data == b'Education deleted'