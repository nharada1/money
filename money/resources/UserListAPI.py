from flask import abort
from flask.ext.restful import Resource, reqparse

from database import db


class UserListAPI(Resource):
    def __init__(self):
        super(UserListAPI, self).__init__()

    def get(self, flightid, userid):
        result = db.get_passenger(flightid, userid)
        return result

