from flask import Flask, make_response, jsonify
from flask.ext.restful import Api
from flask.ext.cors import CORS
from flask.ext.socketio import SocketIO, send, emit
from flask.ext.httpauth import HTTPBasicAuth

from money.resources import FlightAPI, FlightListAPI
from money.resources import UserAPI, UserDenseListAPI, UserListAPI
from money.resources import OfferAPI, OfferListAPI
from money.resources import TransactionAPI, AuthAPI


def init_app():
    money_app = Flask(__name__)
    money_app.debug = True
    CORS(money_app)
    api = Api(money_app)
    api.add_resource(FlightListAPI, '/api/flights/<string:id>', endpoint='flights')
    api.add_resource(FlightAPI, '/api/flight', endpoint='flight')
    api.add_resource(UserAPI, '/api/passenger', endpoint='passenger')
    api.add_resource(UserListAPI, '/api/passengers/<string:flightid>/<string:passid>', endpoint='passengers')
    api.add_resource(UserDenseListAPI, '/api/dense_passenger/<string:flightid>', endpoint='dense_passenger')
    api.add_resource(OfferAPI, '/api/offer', endpoint='offer')
    api.add_resource(OfferListAPI, '/api/flights/<string:flightid>/<string:offerid>', endpoint='offers')
    api.add_resource(TransactionAPI, '/api/transaction', endpoint='transact')

    api.add_resource(AuthAPI, '/api/auth', endpoint='auth')
    socketio = SocketIO(money_app)
    return socketio, money_app

socketio, money_app = init_app()


@money_app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@socketio.on('connect', namespace='/offers')
def connect():
    print('AKJSLJS')
    emit('response', {'data': 'Connected to server'})

def run_server():
    socketio.run(money_app)

if __name__ == "__main__":
    run_server()
