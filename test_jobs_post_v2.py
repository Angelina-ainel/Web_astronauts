import pytest
import requests
from data.db_session import create_session, global_init

base_url = 'http://127.0.0.1:8080'


@pytest.fixture
def db_init():
    global_init('db/mars_explorer.db')


def test_post_job(db_init):
    data = {'team_leader': 2, 'job': 'другая работа', 'work_size': 8, 'collaborators': 'somebody'}
    response = requests.post(base_url + '/api/v2/jobs', json=data)
    assert response.json() == {"success": "OK"}


def test_post_empty(db_init):
    response = requests.post(base_url + '/api/v2/jobs', json={})
    assert response.json() == \
           {"message": {"job": "Missing required parameter in the JSON body or the post body or the query string"}}


def test_post_missed_param(db_init):
    data = {'team_leader': 1, 'work_size': 24}
    response = requests.post(base_url + '/api/v2/jobs', json=data)
    assert response.json() == \
           {"message": {"job": "Missing required parameter in the JSON body or the post body or the query string"}}


def test_post_wrong_param(db_init):
    data = {'team_leader': 2, 'job': 'интересная работа', 'work_size': 'a lot'}
    response = requests.post(base_url + '/api/v2/jobs', json=data)
    assert response.json() == {"message": {"work_size": "invalid literal for int() with base 10: 'a lot'"}}


def test_post_job_double(db_init):
    data = {'id': 1, 'team_leader': 1, 'job': 'описание', 'work_size': 3}
    response = requests.post(base_url + '/api/v2/jobs', json=data)
    assert response.json() == {"error": "Id already exists"}


def test_delete_job(db_init):
    response = requests.delete(base_url + '/api/v2/job/9')
    assert response.json() == {"success": "OK"}











