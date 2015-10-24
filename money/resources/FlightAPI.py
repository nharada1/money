from flask import abort
from flask.ext.restful import Resource, reqparse

from database import db


class FlightAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('flight_id', type=str, location='json')
        super(FlightAPI, self).__init__()

    def post(self):
        args = self.reqparse.parse_args()
        new_id = db.new_flight(args['flight_id'])
        return {'id': new_id}

