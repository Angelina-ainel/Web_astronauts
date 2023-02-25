import pytest
import requests
from data.db_session import create_session, global_init
from data.jobs import Jobs
from flask import jsonify

base_url = 'http://127.0.0.1:5000'


@pytest.fixture
def db_init():
    global_init('db/mars_explorer.db')


def test_get_jobs():
    response = requests.get(base_url + '/api/jobs')
    db_sess = create_session()
    jobs = {'jobs':
            [item.to_dict(only=('id', 'team_leader_relation.email', 'job', 'work_size'))
                 for item in db_sess.query(Jobs).all()]}

    assert response.json() == jobs


def test_get_one_job():
    response = requests.get(base_url + '/api/jobs/1')
    db_sess = create_session()
    job = {'job': db_sess.query(Jobs).get(1).job.to_dict(
        only=('id', 'team_leader_relation.email', 'job', 'work_size', 'collaborators',
              'start_date', 'end_date', 'is_finished', 'team_leader_relation.id',
              'team_leader_relation.email', 'team_leader_relation.name',
              'team_leader_relation.surname'))}
    assert response.json() == job


def test_get_fail_id_job(db_init):
    response = requests.get(base_url + '/api/jobs/999')
    assert response.json() == {"error": "Not Found"}


def test_get_fail_string_job(db_init):
    pass
