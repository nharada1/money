from flask import abort
from flask.ext.restful import Resource, reqparse

from database import db


class OfferListAPI(Resource):
    def __init__(self):
        super(OfferListAPI, self).__init__()

    def get(self, flightid, offerid):
        result = db.get_offer(flightid, offerid)
        return result

