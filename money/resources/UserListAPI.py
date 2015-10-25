from flask import abort
from flask.ext.restful import Resource, reqparse

from database import db


class UserListAPI(Resource):
    def __init__(self):
        super(UserListAPI, self).__init__()

    def get(self, flightid, passid):
        result = db.get_passenger(flightid, passid)
        return result

    def delete(self, flightid, passid):
        result = db.delete_passenger(flightid, passid)
        return result
