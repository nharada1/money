from flask import abort
from flask.ext.restful import Resource, reqparse

from database import db


class FlightAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('flight_id', type=str, location='json')
        super(FlightAPI, self).__init__()

    def get(self, id):
        args = self.reqparse.parse_args()
        result = db.get_flight(id)
