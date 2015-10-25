from flask import abort
from flask.ext.restful import Resource, reqparse

from database import db


class UserAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('passenger_id', type=str, location='json', required=True)
        self.reqparse.add_argument('flight_id', type=str, location='json', required=True)
        self.reqparse.add_argument('row', type=int, location='json', required=True)
        self.reqparse.add_argument('col', type=int, location='json', required=True)
        super(UserAPI, self).__init__()

    def post(self):
        args = self.reqparse.parse_args()
        try:
            flight = db.add_passenger(args['flight_id'], args['passenger_id'], args['row'], args['col'])
            return flight
        except Exception as e:
            print(e)

        return {'error': e}
