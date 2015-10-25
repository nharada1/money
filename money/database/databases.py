import pymongo
import os

from blockchain import blockexplorer
from blockchain.exceptions import APIException

SEAT_COLS = 6


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

    def delete_passenger(self, flight_id, pass_id):
        searched = self.flights.find_one({'_id': flight_id})
        if searched:
            for p in searched['passengers']:
                if p['_id'] == pass_id:
                    try:
                        searched['passengers'].remove(p)
                    except ValueError as v:
                        return {'error': v}
                    self.flights.replace_one({'_id': flight_id}, searched)
                    self._invalidate_offers(flight_id, pass_id)
                    return {'removed': pass_id}
            return {'error': 'Could not find passenger'}
        else:
            return {'error': 'Could not find flight'}

    def get_passenger(self, flight_id, pass_id):
        searched = self.flights.find_one({'_id': flight_id})
        if searched:
            for p in searched['passengers']:
                if p['_id'] == pass_id:
                    return p
            return {'error': 'Could not find passenger'}
        else:
            return {'error': 'Could not find flight'}

    def add_passenger(self, flight_id, pass_id, seat_row, seat_col):
        searched = self.flights.find_one({'_id': flight_id})
        if searched:
            if seat_row >= searched['first_rows'] + searched['econ_rows'] or seat_row < 0:
                return {'error': 'Invalid row'}
            if seat_col > SEAT_COLS or seat_col < 0:
                return {'error': 'Invalid col'}
            new_pass = {'_id': pass_id, 'seat': [seat_row, seat_col]}
            searched['passengers'].append(new_pass)
            self.flights.replace_one({'_id': flight_id}, searched)
            return searched
        else:
            return {'error': 'Could not find flight'}

    def delete_offer(self, flight_id, offerid):
        searched = self.flights.find_one({'_id': flight_id})
        if searched:
            for o in searched['offers']:
                if o['offerid'] == offerid:
                    try:
                        searched['offers'].remove(o)
                    except ValueError as v:
                        return {'error': v}
                    self.flights.replace_one({'_id': flight_id}, searched)
                    return {'removed': offerid}
            return {'error': 'Could not find offer'}
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

    def _invalidate_offers(self, flight_id, passenger):
        """Invalidate all other offers that are going to or from a specific person. We need to do this
        when a transaction goes through, or when a person leaves the server. Return True if we successfully
        invalidate, false if we don't"""
        searched = self.flights.find_one({'_id': flight_id})
        if searched:
            offers = searched['offers']
            for offer in offers:
                if offer['to'] == passenger or offer['fr'] == passenger:
                    offers.remove(offer)
            searched['offers'] = offers
            self.flights.replace_one({'_id': flight_id}, searched)
            return True
        return False


    def transact(self, flightid, offerid, txn_id):
        """Run a transaction. Doing this requires the following to happen:
        1. Validate the offer pending
        2. Check that the txn_id is indeed present in the blockchain (txn has taken place)
        3. Remove the offer from the offer list
        4. Invalidate all other offers for the "to" user (since they've moved seats now)
        5. Update state changed
        """
        searched = self.flights.find_one({'_id': flightid})
        if searched:
            # Validate offer. Remember offers are unique (or at least are supposed to be)
            offer = self.get_offer(flightid, offerid)
            if 'error' in offer:
                return offer
            # Check that the transaction has happened
            try:
                block = blockexplorer.get_tx(txn_id)
            except APIException as e:
                return {'error': 'Bitcoin transaction not found'}
            # Remove offer from the list. We're gonna (unwisely) assume this works with no problems
            self.delete_offer(flightid, offerid)
            # Invalidate other offers.
            tooffers = self._invalidate_offers(flightid, offer['to'])
            fromoffers = self._invalidate_offers(flightid, offer['fr'])
            if not tooffers and not fromoffers:
                return {'Failed to invalidate outstanding transactions'}
            # Update state change. Not sure how we're gonna do that one....
            return {'success': 'Transaction completed (txn {})'.format(txn_id)}
        else:
            return {'error': 'Could not find flight'}
