## API and Events

Reportr uses an HTTP REST API to track events. Datas are always JSON encoded.

| Endpoint | HTTP Method | Description | Arguments |
| -------- | ----------- | ----------- | --------- |
| /api/flights/:flightid | GET | Returns full flight JSON object with this ID |  |
| /api/flight | POST | Add a new flight | `<string>flight_id`  |
| /api/passenger | POST | Add a new passenger to a flight | `<string>flight_id`, `<string>passenger_id` , `<int>row`, `<int>col`|
| /api/passengers/:flightid/:passengerid | GET | Get passenger info by ID | |
| /api/passengers/:flightid/:passengerid | DELETE| Remove a passenger from a flight | |
| /api/offer | POST | Add a new offer to a flight | `<string>to`, `<string>from`, `<string>flight_id`, `<int>price` |
| /api/flights/:flightid/:offerid | GET | Get offer information via ID |  |
| /api/flights/:flightid/:offerid | DELETE | Delete an offer from a flight |  |
| /api/dense_passenger/:flightid| GET | Get a dense version of the passenger matrix |  |
| /api/transaction | POST | Run a transaction in the database | `<string>flight_id`, `<string>offier_id`, `<string>txn_id` |
