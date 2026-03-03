

Updated ER Diagram:

Airline (airline_id PK, airline_name UQ)
City (city_id PK, city_name)
Airport (airport_code PK, city_id FK)
	Airport.city_id REFERENCES City(city_id)
Route (route_id PK, source_id FK, destination_id FK)
	Route.source_id REFERENCES Airport(airport_code)
	Route.destination_id REFERENCES Airport(airport_code)
RouteLeg (route_id PK/FK, leg_number PK, source_id FK, destination_id FK)
	RouteLeg.route_id REFERENCES Route(route_id)
	RouteLeg.source_id REFERENCES Airport(airport_code)
	RouteLeg.destination_id REFERENCES Airport(airport_code)
Fare (fare_id PK, airline_id FK, route_id FK)
	Fare.airline_id REFERENCES Airline(airline_id)
	Fare.route_id REFERENCES Route(route_id)
	UNIQUE (airline_id, route_id)
Info (info_id PK, info_body)
FareObs (obs_id PK, fare_id FK, info_id FK, date, departure_time, arrival_time, arrival_day_offset, duration, total_stops, price)
	FareObs.fare_id REFERENCES Fare(fare_id)
	FareObs.info_id REFERENCES Info(info_id)



Old ER Diagram:

<img width="1371" height="1736" alt="MarlingAmberERDB" src="https://github.com/user-attachments/assets/14402ea0-9b9b-46f7-b27c-55e78e300387" />

see Imgur link if image doesn't load:
https://imgur.com/a/zEsejQs
