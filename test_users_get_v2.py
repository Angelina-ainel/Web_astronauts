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


def test_get_one_user(db_init):
    response = requests.get(base_url + '/api/v2/user/1')
    db_sess = create_session()
    user = db_sess.query(User).get(1)
    assert response.json() == {'user': user.to_dict(rules=('-jobs',))}


def test_get_wrong_user(db_init):
    user_id = 999
    response = requests.get(base_url + f'/api/v2/user/{user_id}')
    assert response.json() == {"message": f"User {user_id} not found"}


def test_get_all_users(db_init):
    response = requests.get(base_url + '/api/v2/users')
    db_sess = create_session()
    users = db_sess.query(User).all()
    assert response.json() == {'users': [item.to_dict(only=('id', 'name', 'surname', 'email', 'jobs.id', 'jobs.job'))
                                         for item in users]}
