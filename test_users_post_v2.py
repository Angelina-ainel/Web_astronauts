import pytest
import requests
from data.db_session import create_session, global_init

base_url = 'http://127.0.0.1:8080'


@pytest.fixture
def db_init():
    global_init('db/mars_explorer.db')


def test_post_user(db_init):
    user_json = {
        'name': 'Имя',
        'surname': 'Фамилия',
        'age': 20,
        'speciality': 'Специальность',
        'email': 'emailtest9@gmail.com'}
    response = requests.post(base_url + '/api/v2/users', json=user_json)
    assert response.json() == {"success": "OK"}


def test_post_user_empty(db_init):
    user_json = {}
    response = requests.post(base_url + '/api/v2/users', json=user_json)
    assert response.json() == {
        "message": {"surname": "Missing required parameter in the JSON body or the post body or the query string"}}


def test_post_user_missed_param(db_init):
    user_json = {
        'surname': 'Фамилия',
        'age': 20,
        'speciality': 'Специальность',
        'email': 'emailtest2@gmail.com'}
    response = requests.post(base_url + '/api/v2/users', json=user_json)
    assert response.json() == {
        "message": {"name": "Missing required parameter in the JSON body or the post body or the query string"}}


def test_post_user_wrong_param(db_init):
    user_json = {
        'name': 'Има',
        'surname': 'Фамилия',
        'age': 'age',
        'speciality': 'Специальность',
        'email': 'emailtest3@gmail.com'}
    response = requests.post(base_url + '/api/v2/users', json=user_json)
    assert response.json() == {"message": {"age": "invalid literal for int() with base 10: 'age'"}}


def test_post_user_already_exists(db_init):
    user_json = {
        'id': 5,
        'name': 'Имя',
        'surname': 'Фамилия',
        'age': 20,
        'speciality': 'Специальность',
        'email': 'emailtest4@gmail.com'}
    response = requests.post(base_url + '/api/v2/users', json=user_json)
    assert response.json() == {"error": "Id already exists"}


def test_delete_user(db_init):
    response = requests.delete(base_url + '/api/v2/user/9')
    assert response.json() == {"success": "OK"}
