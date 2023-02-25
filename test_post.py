import pytest
import requests
from data.db_session import create_session, global_init
from data.jobs import Jobs
import json
from flask import jsonify

base_url = 'http://127.0.0.1:5000'


@pytest.fixture
def db_init():
    global_init('db/mars_explorer.db')


def test_post_job(db_init):
    data = {'team_leader': 1, 'job': 'описание', 'work_size': 3}
    response = requests.post(base_url + '/api/jobs', json=data)
    assert response.json() == {{'success': 'OK'}}
    db_sess = create_session()
    jobs = {'jobs':
            [item.to_dict(only=('id', 'team_leader_relation.email', 'job', 'work_size'))
                 for item in db_sess.query(Jobs).all()]}

    assert response.json() == jobs


def test_post_empty(db_init):
    response = requests.post(base_url + '/api/jobs', json={})
    assert response.json() == {'error': 'Empty request'}


def test_post_bad_job(db_init):
    data = {'team_leader': 1, 'job': 'описание'}
    response = requests.post(base_url + '/api/jobs', json=data)
    assert response.json() == {'error': 'Bad request'}


def test_post_job_double(db_init):
    data = {'id': 1, 'team_leader': 1, 'job': 'описание', 'work_size': 3}
    response = requests.post(base_url + '/api/jobs', json=data)
    assert response.json() == {'error': 'Id already exists'}











