import uuid
import pymongo
import os
from datetime import datetime


class MongoDB():
    def __init__(self):
        """MongoDB bindings"""
        self.uri = os.environ.get('MONGOLAB_URI')
        self.flights = None
        self.init_connection()

    def init_connection(self):
        client = pymongo.MongoClient(self.uri)
        default_db = client.get_default_database()
        self.flights = default_db.flights

    def new_flight(self, flight_data):
        flight_data['_id'] = "{}{}".format(flight_data['airline'], flight_data['flight_no'])
        flight_data['passengers'] = []
        flight_data['offers'] = []
        returned_id = self.flights.insert_one(flight_data).inserted_id
        return returned_id

    def get_flight(self, flight_id):
        searched = self.flights.find_one({'_id': flight_id})
        if searched:
            return searched
        else:
            return {'error': 'Could not find flight'}

    def get_offer(self, flight_id, offer_id):
        searched = self.flights.find_one({'_id': flight_id})
        if searched:
            for s in searched['offers']:
                if s['offerid'] == offer_id:
                    return s
            return {'error': 'Could not find offer with this id'}
        else:
            return {'error': 'Could not find flight'}

    def add_passenger(self, flight_id, pass_id, seat_row, seat_col):
        searched = self.flights.find_one({'_id': flight_id})
        if searched:
            new_pass = {'_id': pass_id, 'seat': [seat_row, seat_col]}
            searched['passengers'].append(new_pass)
            self.flights.replace_one({'_id': flight_id}, searched)
            return searched
        else:
            return {'error': 'Could not find flight'}

    def add_offer(self, flight_id, to, fr, price):
        searched = self.flights.find_one({'_id': flight_id})
        if searched:
            # Ensure to and from are valid users on this plane
            ids = [v['_id'] for v in searched['passengers']]
            if to not in ids and fr not in ids:
                return {'error': 'Both passengers are not on this flight'}

            offerids = [v['offerid'] for v in searched['offers']]
            offerid = "{}{}".format(fr, to)
            if offerid in offerids:
                return {'error': 'This offer is already in the database'}

            new_offer = {'offerid': offerid, 'to': to, 'fr': fr, 'price': price}
            searched['offers'].append(new_offer)
            self.flights.replace_one({'_id': flight_id}, searched)
            return offerid
        else:
            return {'error': 'Could not find flight'}
