from flask import abort
from flask.ext.restful import Resource, reqparse

from database import db


class FlightListAPI(Resource):
    def __init__(self):
        super(FlightListAPI, self).__init__()

    def get(self, id):
        result = db.get_flight(id)
        return result

