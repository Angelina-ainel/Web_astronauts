from flask_restful import abort, Resource
from flask import jsonify
from data import db_session
from data.jobs import Jobs
from jobs_parser import parser


def get_or_abort_if_job_is_not_found(job_id):
    session = db_session.create_session()
    job = session.query(Jobs).get(job_id)
    if not job:
        abort(404, message=f"Job {job_id} is not found")
    return session, job


class JobsResource(Resource):
    def get(self, job_id):
        session, job = get_or_abort_if_job_is_not_found(job_id)
        return jsonify({'job': job.to_dict(rules=('-team_leader_relation', ))})

    def delete(self, job_id):
        session, job = get_or_abort_if_job_is_not_found(job_id)
        session.delete(job)
        session.commit()
        return jsonify({"success": "OK"})


class JobsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        jobs = session.query(Jobs).all()
        return jsonify({'jobs': [job.to_dict(
            only=('id', 'team_leader_relation.name', 'team_leader_relation.surname', 'job', 'work_size'))
            for job in jobs]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        job = session.query(Jobs).get(args.get('id'))
        if job:
            return jsonify({"error": "Id already exists"})
        job = Jobs(**args)
        session.add(job)
        session.commit()

        return jsonify({"success": "OK"})
