from flask import abort
from flask.ext.restful import Resource, reqparse

from bs4 import BeautifulSoup
import urllib.request
from database import db


class FlightAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('flight_id', type=str, location='json', required=True)
        super(FlightAPI, self).__init__()

    def get_airline_info(self, flightid):
        url = 'https://flightaware.com/live/flight/' + str(flightid)
        with urllib.request.urlopen(url) as response:
            html = response.read()
        soup = BeautifulSoup(html, 'html.parser')
        title = soup.findAll("div", { "class" : "track-panel-header-title" })
        airline, flight_no = title[0].span.text.strip().split(' ')
        time = soup.findAll("tr", { "class" : "track-panel-scheduledtime"})
        takeoff = time[0].td.text.strip().split('\xa0')[0]
        landing = time[1].td.text.strip().split('\xa0')[0]
        depart = soup.findAll("td", { "class": "track-panel-departure"})
        fr = depart[0].span.text
        arrive = soup.findAll("td", { "class": "track-panel-arrival"})
        to = arrive[0].span.text
        airline_dict = {'airline': airline, 'flight_no': int(flight_no), 'to': to, 'from': fr, 'takeoff': takeoff, 'landing': landing}
        # make some assumptions
        airline_dict['model'] = "Airbus 320"
        airline_dict['first_rows'] = 3
        airline_dict['econ_rows'] = 22
        return airline_dict

    def post(self):
        args = self.reqparse.parse_args()
        try:
            airline = self.get_airline_info(args['flight_id'])
            new_id = db.new_flight(airline)
            return {'id': new_id}
        except Exception as e:
            print(e)
            return {'error': e}


