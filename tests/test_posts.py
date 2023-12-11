from instance.config import TESTING_HEADER, SECOND_USER_TESTING_HEADER


def test_create_post_all_fields_correct(client):
    post_form_data = {
        'post_title' : "test_title",
        'post_caption' : "test_caption"
    }

    response = client.post("/post/",
                           data = post_form_data,
                           headers = TESTING_HEADER)
    
    assert response.status_code == 200

    assert response.data == b'{"post_caption":"test_caption","post_id":1,"post_title":"test_title","post_user_id":1}\n'

def test_create_post_missing_fields(client):
    post_missing_data = {
        'post_title' : "test_title",
    }

    response = client.post("/post/",
                           data = post_missing_data,
                           headers = TESTING_HEADER)
    
    assert response.status_code == 400

    assert response.data == b"""All details have not been sent. Required Fields :
                                              post_title, post_caption."""

def test_get_post_correct_post_id(client):
    response = client.get("/post/1", headers = TESTING_HEADER)

    assert response.status_code == 200

    assert response.data == b'{"post_caption":"test_caption","post_id":1,"post_title":"test_title","post_user_id":1}\n'

def test_get_post_incorrect_post_id(client):
    response = client.get("/post/5", headers = TESTING_HEADER)
    
    assert response.status_code == 400

    assert response.data ==  b"Post Id given doesn't match any existing post" 

def test_update_post(client):
    post_update_data = {
        'post_title' : "first_update_test_title",
        'post_caption' : "first_update_test_caption"
    }

    response = client.put("/post/1", data =post_update_data, headers = TESTING_HEADER)

    assert response.status_code == 200

    assert response.data == b'{"post_caption":"first_update_test_caption","post_id":1,"post_title":"first_update_test_title","post_user_id":1}\n'


def test_update_post_absent_access_token(client):
    post_update_data = {
        'post_title' : "absent_token_update_test_title",
        'post_caption' : "absent_token_update_test_caption"
    }

    response = client.put("/post/1", data =post_update_data)

    assert response.status_code == 400

    assert response.data == b'No User Found. Login first.'

def test_update_post_malformed_token(client):
    post_update_data = {
        'post_title' : "malformed_token_update_test_title",
        'post_caption' : "malformed_token_update_test_caption"
    }

    response = client.put("/post/1", data = post_update_data, headers = {'x-access-token':"123"})

    assert response.status_code == 400
    assert response.data == b'Malformed Token sent'

def test_delete_post_invalid_post_id(client):

    response = client.delete("/post/5", headers = TESTING_HEADER)

    assert response.status_code == 400

    assert response.data == b"Post Id given doesn't match any existing post" 

def test_delete_post_malformed_access_token(client):
    
    response = client.delete("/post/1", headers = {'x-access-token':'123'})

    assert response.status_code == 400

    assert response.data == b'Malformed Token sent'

def test_delete_post_absent_access_token(client):
    
    response = client.delete("/post/1")

    assert response.status_code == 400

    assert response.data == b'No User Found. Login first.'

def test_delete_post_invalid_access(client):

    response = client.delete("/post/1", headers = SECOND_USER_TESTING_HEADER)

    assert response.status_code == 400

    assert response.data == b"You don't have permissions to delete this post"

def test_delete_post_valid_data(client):

    response = client.delete("/post/1", headers = TESTING_HEADER)

    assert response.status_code == 200

    assert response.data == b'Post Deleted'

