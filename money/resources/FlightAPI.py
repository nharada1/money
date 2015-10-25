from flask import abort
from flask.ext.restful import Resource, reqparse

from database import db


class FlightAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('airline', type=str, location='json', required=True)
        self.reqparse.add_argument('flight_no', type=int, location='json', required=True)
        self.reqparse.add_argument('date', type=str, location='json', required=True)
        self.reqparse.add_argument('from', type=str, location='json', required=True)
        self.reqparse.add_argument('to', type=str, location='json', required=True)
        self.reqparse.add_argument('takeoff', type=str, location='json', required=True)
        self.reqparse.add_argument('landing', type=str, location='json', required=True)
        self.reqparse.add_argument('model', type=str, location='json', required=True)
        self.reqparse.add_argument('first_rows', type=int, location='json', required=True)
        self.reqparse.add_argument('econ_rows', type=int, location='json', required=True)
        super(FlightAPI, self).__init__()

    def post(self):
        args = self.reqparse.parse_args()
        try:
            new_id = db.new_flight(args)
        except Exception as e:
            print(e)

        return {'id': new_id}

