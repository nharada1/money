import uuid
import pymongo
import os
from datetime import datetime


class MongoDB():
    def __init__(self):
        """MongoDB bindings"""
        self.uri = os.environ.get('MONGOLAB_URI')
        self.init_connection()
        self.flights = None

    def init_connection(self):
        client = pymongo.MongoClient(self.uri)
        default_db = client.get_default_database()
        self.flights = default_db.flights

    def new_flight(self, flight_id):
        flight = {'_id': flight_id}
        returned_id = self.flights.insert_one(flight).inserted_id
        return returned_id

    def get_flight(self, flight_id):
        searched = self.flights.find_one({'_id': flight_id})
        return searched

    def add_passenger(self, flight_id):
        pass
