from flask import abort
from flask.ext.restful import Resource, reqparse

from database import db


class UserDenseListAPI(Resource):
    def __init__(self):
        super(UserDenseListAPI, self).__init__()

    def _search_by_row(self, passengers, row):
        passes = []
        for p in passengers:
            if p['seat'][0] == row:
                passes.append(p)
        return passes

    def _search_by_col(self, passengers, col):
        passes = []
        for p in passengers:
            if p['seat'][1] == col:
                passes.append(p)
        return passes

    def get(self, flightid):
        flight = db.get_flight(flightid)
        passengers = flight['passengers']
        n_first = flight['first_rows']
        n_econ = flight['econ_rows']
        n_across = 6 # Hardcored for now

        dense = []
        for row in range(n_first+n_econ):
            passes = self._search_by_row(passengers, row)
            row_data = []
            for col in range(n_across):
                this_pass = self._search_by_col(passes, col)
                if this_pass:
                    cur_pass = this_pass
                else:
                    cur_pass = {'_id': '', 'seat': [row, col], 'flight_id': flightid}
                row_data.append(cur_pass)
            dense.append(row_data)
        print(dense)
        return dense


