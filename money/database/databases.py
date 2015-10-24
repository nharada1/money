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
        print(flight_data)
        returned_id = self.flights.insert_one(flight_data).inserted_id
        return returned_id

    def get_flight(self, flight_id):
        searched = self.flights.find_one({'_id': flight_id})
        return searched

    def add_passenger(self, flight_id):
        pass
