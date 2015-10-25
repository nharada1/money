from flask import abort
from flask.ext.restful import Resource, reqparse

from database import db


class OfferAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('flight_id', type=str, location='json', required=True)
        self.reqparse.add_argument('to', type=str, location='json', required=True)
        self.reqparse.add_argument('from', type=str, location='json', required=True)
        self.reqparse.add_argument('price', type=int, location='json', required=True)
        super(OfferAPI, self).__init__()

    def post(self):
        args = self.reqparse.parse_args()
        try:
            offer = db.add_offer(args['flight_id'], args['to'], args['from'], args['price'])
            return offer
        except Exception as e:
            print(e)

        return {'error': e}