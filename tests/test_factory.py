from backend import create_app


def test_config():
    db_path = "sqlite:///project.db"
    assert not create_app().testing
    assert create_app({'TESTING': True,
                       'SQLALCHEMY_DATABASE_URI': db_path}).testing


def test_hello(client):
    response = client.get('/hello')
    assert response.status_code == 404