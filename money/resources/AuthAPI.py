from flask import abort
from flask.ext.restful import Resource, reqparse

from database import db


class AuthAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('username', type=str, required=True)
        self.reqparse.add_argument('password', type=str, required=True)
        super(AuthAPI, self).__init__()

    def get(self):
        args = self.reqparse.parse_args()
        user = args['username']
        hashed_pass = args['password']
        # I want to die
        return db.get_user(user, hashed_pass)

    def post(self):
        args = self.reqparse.parse_args()
        try:
            user = args['username']
            hashed_pass = args['password']
            offer = db.new_user(user, hashed_pass)
            return offer
        except Exception as e:
            print(e)
            return {'error': e}
