from flask_restful import reqparse, abort, Api, Resource
from flask import jsonify
from ..data import db_session
from data.users import User
from user_parser import parser


def get_or_abort_if_user_not_found(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        abort(404, message=f"User {user_id} not found")
    return user


class UsersResource(Resource):
    def get(self, user_id):
        user = get_or_abort_if_user_not_found(user_id)
        return jsonify({'user': user.to_dict(rules=('-jobs', ))})

    def delete(self, news_id):
        user = get_or_abort_if_user_not_found(news_id)
        session = db_session.create_session()
        session.delete(user)
        session.commit()
        return jsonify({"success": "OK"})


class UsersListResource(Resource):
    def get(self):
        session = db_session.create_session()
        users = session.query(User).all()
        return jsonify({'users': [user.to_dict(
            only=('id', 'name', 'surname', 'email', 'jobs.id', 'jobs.job')) for user in users]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        user = User(id=args.get('id'),
                    surname=args['surname'],
                    name=args['name'],
                    age=args['age'],
                    position=args.get('position'),
                    speciality=args['speciality'],
                    address=args.get('address'),
                    email=args['email'])
        session.add(user)
        session.commit()
        return jsonify({'success': 'OK'})
