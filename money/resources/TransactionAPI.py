from flask import abort
from flask.ext.restful import Resource, reqparse

from database import db


class TransactionAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('flight_id', type=str, location='json', required=True)
        self.reqparse.add_argument('offer_id', type=str, location='json', required=True)
        self.reqparse.add_argument('txn_id', type=str, location='json', required=True)
        super(TransactionAPI, self).__init__()

    def post(self):
        args = self.reqparse.parse_args()
        try:
            result = db.transact(args['flight_id'], args['offer_id'], args['txn_id'])
            return result
        except Exception as e:
            raise
            print(e)
            return {'error': e}

