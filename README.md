## API and Events

Reportr uses an HTTP REST API to track events. Datas are always JSON encoded.

| Endpoint | HTTP Method | Description | Arguments |
| -------- | ----------- | ----------- | --------- |
| /api/flights/:flightid | GET | Returns full flight JSON object with this ID |  |
| /api/flight | POST | Add a new flight |  |
| /api/passenger | POST | Add a new passenger to a flight | `<string>type`, `<object>properties` |
| /api/passengers/:passengerid | GET | Get passenger info by ID | `<string>type`, `<object>properties` |
| /api/passengers/:passengerid | DELETE| Remove a passenger from a flight | `<string>type`, `<object>properties` |
| /api/offer | POST | Add a new offer to a flight | `<string>type`, `<int>start(0)`, `<int>limit` |
| /api/offers/:offerid | GET | Get offer information via ID | `<string>type`, `<int>start(0)`, `<int>limit` |
| /api/offers/:offerid | DELETE | Delete an offer from a flight | `<string>type`, `<int>start(0)`, `<int>limit` |
