import pytest
import requests
from data.db_session import create_session, global_init
from data.jobs import Jobs
from flask import jsonify

base_url = 'http://127.0.0.1:8080'


@pytest.fixture
def db_init():
    global_init('db/mars_explorer.db')


def test_get_jobs(db_init):
    response = requests.get(base_url + '/api/v2/jobs')
    db_sess = create_session()
    jobs = {'jobs':
        [item.to_dict(
            only=('id', 'team_leader_relation.name', 'team_leader_relation.surname', 'job', 'work_size'))
            for item in db_sess.query(Jobs).all()]}
    assert response.json() == jobs


def test_get_one_job(db_init):
    response = requests.get(base_url + '/api/v2/job/1')
    db_sess = create_session()
    job = db_sess.query(Jobs).get(1)
    assert response.json() == {'job': job.to_dict(rules=('-team_leader_relation',))}


def test_get_wrong_job(db_init):
    job_id = 999
    response = requests.get(base_url + f'/api/v2/job/{job_id}')
    assert response.json() == {"message": f"Job {job_id} is not found"}


# def test_get_fail_string_job(db_init):
#     response = requests.get(base_url + '/api/v2/job/string')
#     assert response.json() == {"error": "Not Found"}
