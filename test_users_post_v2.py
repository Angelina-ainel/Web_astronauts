import pytest
import requests
from data.db_session import create_session, global_init
from data.jobs import Jobs
from data.users import User
import json
from flask import jsonify

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
        'email': 'emailtest1@gmail.com'}
    response = requests.post(base_url + '/api/v2/users', json=user_json)
    assert response.json() == {"success": "OK"}


def test_post_user_empty(db_init):
    user_json = {}
    response = requests.post(base_url + '/api/v2/users', json=user_json)
    assert response.json() == {"message": "error"}


def test_post_user_missed_param(db_init):
    user_json = {}


def test_post_user_wrong_param(db_init):
    user_json = {}


def test_post_user_already_exists(db_init):
    pass


def test_delete_user(db_init):
    response = requests.delete(base_url + '/api/v2/user/2')
    assert response.json() == {"success": "OK"}
