from instance.config import TESTING_HEADER, SECOND_USER_TESTING_HEADER
import json

def test_create_quiz(client):

    quiz_json_data = {
        "quiz_title" : "abc",
        "quiz_caption" : "first_quiz",
        "quiz_questions" : {
            1 : {
                "question_text" : "first question",
                "question_answer" : 1,
                "options" : {
                    1:{
                        "sequence_id" : 1,
                        "text" : "first option"
                    },
                    2:{
                        "sequence_id" : 2,
                        "text" : "second option"
                    }
                }
            },
            2: {
                "question_text" : "first question",
                "question_answer" : 1,
                "options" : {
                    1:{
                        "sequence_id" : 1,
                        "text" : "first option"
                    }
                }
            }
        }
    }

    response = client.post("/quiz/", data= json.dumps(quiz_json_data),
                            headers = TESTING_HEADER,
                            content_type = 'application/json')

    
    assert response.status_code == 200
    assert response.data == b'{"quiz_caption":"first_quiz","quiz_id":1,"quiz_questions":{"1":{"options":{"1":{"option_id":1,"option_sequence_id":1,"option_text":"first option"},"2":{"option_id":2,"option_sequence_id":2,"option_text":"second option"}},"question_id":1,"question_text":"first question"},"2":{"options":{"1":{"option_id":3,"option_sequence_id":1,"option_text":"first option"}},"question_id":2,"question_text":"first question"}},"quiz_title":"abc","quiz_user_id":1}\n'



def test_get_quiz(client):

    response = client.get('/quiz/1', headers = TESTING_HEADER)

    assert response.status_code == 200
    assert response.data == b'{"quiz_caption":"first_quiz","quiz_id":1,"quiz_questions":{"1":{"options":{"1":{"option_id":1,"option_sequence_id":1,"option_text":"first option"},"2":{"option_id":2,"option_sequence_id":2,"option_text":"second option"}},"question_id":1,"question_text":"first question"},"2":{"options":{"1":{"option_id":3,"option_sequence_id":1,"option_text":"first option"}},"question_id":2,"question_text":"first question"}},"quiz_title":"abc","quiz_user_id":1}\n'

def test_update_quiz(client):
    updated_quiz_json_data = {
    "quiz_title" : "abc",
    "quiz_caption" : "updated_quiz",
    "quiz_questions" : {
        "1" : {
            "question_text" : "updated question",
            "question_answer" : 1,
            "options" : {
                "1":{
                    "sequence_id" : 1,
                    "text" : "updated option"
                },
                "2":{
                    "sequence_id" : 2,
                    "text" : "second option"
                }
            }
        },
        "2": {
            "question_text" : "second question",
            "question_answer" : 1,
            "options" : {
                "1":{
                    "sequence_id" : 1,
                    "text" : "second option"
                }
            }
        },
        "3" : {
            "question_text" : "updated question",
            "question_answer" : 1,
            "options" : {
                "1":{
                    "sequence_id" : 1,
                    "text" : "updated option"
                },
                "2":{
                    "sequence_id" : 2,
                    "text" : "second option"
                }
            }
        }
    }
}
    
    response = client.put('/quiz/1', headers = TESTING_HEADER,
                          data= json.dumps(updated_quiz_json_data),
                          content_type = 'application/json')
    
    assert response.status_code == 200
    assert response.data ==  b'{"quiz_caption":"updated_quiz","quiz_id":1,"quiz_questions":{"1":{"options":{"1":{"option_id":1,"option_sequence_id":1,"option_text":"updated option"},"2":{"option_id":2,"option_sequence_id":2,"option_text":"second option"}},"question_id":1,"question_text":"updated question"},"2":{"options":{"1":{"option_id":3,"option_sequence_id":1,"option_text":"second option"}},"question_id":2,"question_text":"second question"},"3":{"options":{"1":{"option_id":4,"option_sequence_id":1,"option_text":"updated option"},"2":{"option_id":5,"option_sequence_id":2,"option_text":"second option"}},"question_id":3,"question_text":"updated question"}},"quiz_title":"abc","quiz_user_id":1}\n'

def test_delete_quiz(client):
    response = client.delete('/quiz/1', headers = TESTING_HEADER)

    assert response.status_code == 200
    assert response.data == b'Quiz Deleted'