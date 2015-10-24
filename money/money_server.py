from flask import Flask, make_response, jsonify
from flask.ext.restful import Api
from flask.ext.cors import CORS

from money.resources import FlightAPI, FlightListAPI


def init_app():
    money_app = Flask(__name__)
    CORS(money_app)
    api = Api(money_app)
    api.add_resource(FlightListAPI, '/api/flights/<string:id>', endpoint='flights')
    api.add_resource(FlightAPI, '/api/flight', endpoint='flight')
    return money_app

money_app = init_app()


@money_app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


def run_server():
    money_app.run(debug=True)

if __name__ == "__main__":
    run_server()
