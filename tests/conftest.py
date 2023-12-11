import sqlite3

import pytest
from backend import create_app
from instance.config import INSTANCE_PATH
#from flaskr.db import get_db, init_db

"""with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')"""


@pytest.fixture(scope='session', autouse= True)
def app():
    db_path = "sqlite:///test.db"

    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': db_path,
    })

    """with app.app_context():
        init_db()
        get_db().executescript(_data_sql)
    """
    yield app
    
    



@pytest.fixture(scope="session", autouse= True)
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()

@pytest.fixture(scope="session", autouse= True)
def cleanup(request):
    def delete_data_from_test_db():
        conn = sqlite3.connect(INSTANCE_PATH + r'\test.db')
        cursor = conn.cursor()
        cursor.execute('DELETE from user;')
        cursor.execute('DELETE from education')
        cursor.execute('DELETE from quiz')
        cursor.execute('DELETE from option')
        cursor.execute('DELETE from post')
        cursor.execute('DELETE from profession')
        cursor.execute('DELETE from question')
        conn.commit()
        conn.close()
    request.addfinalizer(delete_data_from_test_db)


@pytest.fixture(scope="session", autouse= True)
def create_test_user(client):
    signup_form_data = {
        "first_name" : "abc",
        "last_name" : "xyz",
        "email" : "abc@xyz.com",
        "password" : "123456"
    }

    response = client.post("/auth/register",data = signup_form_data)

    assert response.status_code == 200
    assert response.data == b'User created'

    second_user_signup_form_data = {
        "first_name" : "123",
        "last_name" : "456",
        "email" : "123@456.com",
        "password" : "abcdef"
    }

    response = client.post("/auth/register",data = second_user_signup_form_data)

    assert response.status_code == 200
    assert response.data == b'User created'