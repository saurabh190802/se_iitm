from instance.config import TESTING_HEADER, SECOND_USER_TESTING_HEADER

def test_create_profession(client):
    profession_form_data = {
        'company_name' : 'test_company',
        'joining_year' : 2000,
        'graduation_year' : 2004
    }

    response = client.post('/achievement/profession', data = profession_form_data,
                           headers = TESTING_HEADER)
    
    assert response.status_code == 200

    assert response.data == b'{"company_name":"test_company","graduation_year":"2004","joining_year":"2000","profession_id":1,"user_id":1}\n'


def test_create_profession_missing_fields(client):
    missing_profession_form_data = {
        'company_name' : 'test_company',
        'joining_year' : 2000
    }

    response = client.post('/achievement/profession', data = missing_profession_form_data,
                           headers = TESTING_HEADER)
    
    assert response.status_code == 400

    assert response.data ==  b"""All details have not been sent. Required Fields :
                                            company_name, joining_year, graduation_year"""
    

def test_create_profession_absent_token(client):
    profession_form_data = {
        'company_name' : 'test_company',
        'joining_year' : 2000,
        'graduation_year' : 2004
    }

    response = client.post('/achievement/profession', data = profession_form_data)

    
    
    assert response.status_code == 400

    assert response.data ==  b'No User Found. Login first.'

def test_create_profession_malformed_token(client):
    profession_form_data = {
        'company_name' : 'test_company',
        'joining_year' : 2000,
        'graduation_year' : 2004
    }

    response = client.post('/achievement/profession', data = profession_form_data,
                           headers = {'x-access-token':'abc'})

    
    
    assert response.status_code == 400

    assert response.data ==  b'Malformed Token sent'

def test_get_profession_valid_id(client):

    response = client.get('/achievement/profession/1', headers = TESTING_HEADER)

    assert response.status_code == 200

    assert response.data == b'{"company_name":"test_company","graduation_year":2004,"joining_year":2000,"profession_id":1,"user_id":1}\n'


def test_get_profession_invalid_id(client):

    response = client.get('/achievement/profession/6', headers = TESTING_HEADER)

    assert response.status_code == 400

    assert response.data == b"Profession Id given doesn't match any existing entry"

def test_get_profession_absent_client_token(client):

    response = client.get('/achievement/profession/1')

    assert response.status_code == 400

    assert response.data == b'No User Found. Login first.'

def test_update_profession_valid(client):
    
    update_profession_form_data = {
        'company_name' : 'update_test_company',
        'joining_year' : 2010,
        'graduation_year' : 2014
    }

    response = client.put('/achievement/profession/1', data = update_profession_form_data,
                          headers = TESTING_HEADER)
    
    assert response.status_code == 200

    assert response.data == b'{"company_name":"update_test_company","graduation_year":2014,"joining_year":2010,"profession_id":1,"user_id":1}\n'

def test_update_profession_invalid_id(client):

    update_profession_form_data = {
        'company_name' : 'update_test_company',
        'joining_year' : 2010,
        'graduation_year' : 2014
    }

    response = client.put('/achievement/profession/5', data = update_profession_form_data,
                          headers = TESTING_HEADER)
    
    assert response.status_code == 400

    assert response.data == b"Profession Id given doesn't match any existing entry"

def test_update_profession_invalid_access(client):

    update_profession_form_data = {
        'company_name' : 'update_test_company',
        'joining_year' : 2010,
        'graduation_year' : 2014
    }

    response = client.put('/achievement/profession/1', data = update_profession_form_data,
                          headers = SECOND_USER_TESTING_HEADER)
    
    assert response.status_code == 400

    assert response.data == b"You don't have permissions to update this entry."


def test_delete_profession_invalid_id(client):

    response = client.delete('/achievement/profession/5', headers = TESTING_HEADER)

    assert response.status_code == 400

    assert response.data == b"Profession Id given doesn't match any existing entry"

def test_delete_profession_invalid_access(client):

    response = client.delete('/achievement/profession/1', headers = SECOND_USER_TESTING_HEADER)

    assert response.status_code == 400

    assert response.data == b"You don't have permissions to delete this entry."

def test_delete_profession_valid(client):

    response = client.delete('/achievement/profession/1', headers = TESTING_HEADER)

    assert response.status_code == 200

    assert response.data == b'Profession deleted'