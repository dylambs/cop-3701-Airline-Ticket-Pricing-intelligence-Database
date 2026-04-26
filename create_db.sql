-- create_db.sql
-- Oracle schema for the airline ticket pricing database.
-- This version matches dataload.py / dataload1.py and the cleaned CSV files.
-- Run this file with F5 / Run Script in SQL Developer.

BEGIN
    EXECUTE IMMEDIATE 'DROP TABLE FareObs CASCADE CONSTRAINTS PURGE';
EXCEPTION
    WHEN OTHERS THEN
        IF SQLCODE != -942 THEN RAISE; END IF;
END;
/

BEGIN
    EXECUTE IMMEDIATE 'DROP TABLE Fare CASCADE CONSTRAINTS PURGE';
EXCEPTION
    WHEN OTHERS THEN
        IF SQLCODE != -942 THEN RAISE; END IF;
END;
/

BEGIN
    EXECUTE IMMEDIATE 'DROP TABLE RouteLeg CASCADE CONSTRAINTS PURGE';
EXCEPTION
    WHEN OTHERS THEN
        IF SQLCODE != -942 THEN RAISE; END IF;
END;
/

BEGIN
    EXECUTE IMMEDIATE 'DROP TABLE Route CASCADE CONSTRAINTS PURGE';
EXCEPTION
    WHEN OTHERS THEN
        IF SQLCODE != -942 THEN RAISE; END IF;
END;
/

BEGIN
    EXECUTE IMMEDIATE 'DROP TABLE Airport CASCADE CONSTRAINTS PURGE';
EXCEPTION
    WHEN OTHERS THEN
        IF SQLCODE != -942 THEN RAISE; END IF;
END;
/

BEGIN
    EXECUTE IMMEDIATE 'DROP TABLE City CASCADE CONSTRAINTS PURGE';
EXCEPTION
    WHEN OTHERS THEN
        IF SQLCODE != -942 THEN RAISE; END IF;
END;
/

BEGIN
    EXECUTE IMMEDIATE 'DROP TABLE Airline CASCADE CONSTRAINTS PURGE';
EXCEPTION
    WHEN OTHERS THEN
        IF SQLCODE != -942 THEN RAISE; END IF;
END;
/

BEGIN
    EXECUTE IMMEDIATE 'DROP TABLE Info CASCADE CONSTRAINTS PURGE';
EXCEPTION
    WHEN OTHERS THEN
        IF SQLCODE != -942 THEN RAISE; END IF;
END;
/

CREATE TABLE Airline (
    airline_id      NUMBER PRIMARY KEY,
    airline_name    VARCHAR2(100) NOT NULL
);

CREATE TABLE City (
    city_id     NUMBER PRIMARY KEY,
    city_name   VARCHAR2(100) NOT NULL
);

CREATE TABLE Airport (
    airport_code    VARCHAR2(10) PRIMARY KEY,
    city_id         NUMBER NOT NULL,
    CONSTRAINT fk_airport_city
        FOREIGN KEY (city_id) REFERENCES City(city_id)
);

CREATE TABLE Route (
    route_id         NUMBER PRIMARY KEY,
    source_id        VARCHAR2(10) NOT NULL,
    destination_id   VARCHAR2(10) NOT NULL,
    CONSTRAINT fk_route_source
        FOREIGN KEY (source_id) REFERENCES Airport(airport_code),
    CONSTRAINT fk_route_destination
        FOREIGN KEY (destination_id) REFERENCES Airport(airport_code),
    CONSTRAINT chk_route_not_same
        CHECK (source_id <> destination_id)
);

CREATE TABLE RouteLeg (
    route_id         NUMBER NOT NULL,
    leg_number       NUMBER NOT NULL,
    source_id        VARCHAR2(10) NOT NULL,
    destination_id   VARCHAR2(10) NOT NULL,
    CONSTRAINT pk_routeleg PRIMARY KEY (route_id, leg_number),
    CONSTRAINT fk_routeleg_route
        FOREIGN KEY (route_id) REFERENCES Route(route_id),
    CONSTRAINT fk_routeleg_source
        FOREIGN KEY (source_id) REFERENCES Airport(airport_code),
    CONSTRAINT fk_routeleg_destination
        FOREIGN KEY (destination_id) REFERENCES Airport(airport_code),
    CONSTRAINT chk_routeleg_not_same
        CHECK (source_id <> destination_id)
);

CREATE TABLE Fare (
    fare_id     NUMBER PRIMARY KEY,
    airline_id  NUMBER NOT NULL,
    route_id    NUMBER NOT NULL,
    CONSTRAINT fk_fare_airline
        FOREIGN KEY (airline_id) REFERENCES Airline(airline_id),
    CONSTRAINT fk_fare_route
        FOREIGN KEY (route_id) REFERENCES Route(route_id)
);

CREATE TABLE Info (
    info_id     NUMBER PRIMARY KEY,
    info_body   VARCHAR2(200) NOT NULL
);

CREATE TABLE FareObs (
    obs_id              NUMBER PRIMARY KEY,
    fare_id             NUMBER NOT NULL,
    info_id             NUMBER NOT NULL,
    journey_date        DATE NOT NULL,
    departure_time      VARCHAR2(20) NOT NULL,
    arrival_time        VARCHAR2(20) NOT NULL,
    arrival_day_offset  NUMBER DEFAULT 0 NOT NULL,
    duration_minutes    NUMBER NOT NULL,
    total_stops         NUMBER NOT NULL,
    price               NUMBER(10,2) NOT NULL,
    CONSTRAINT fk_fareobs_fare
        FOREIGN KEY (fare_id) REFERENCES Fare(fare_id),
    CONSTRAINT fk_fareobs_info
        FOREIGN KEY (info_id) REFERENCES Info(info_id),
    CONSTRAINT chk_fareobs_day_offset
        CHECK (arrival_day_offset >= 0),
    CONSTRAINT chk_fareobs_duration
        CHECK (duration_minutes >= 0),
    CONSTRAINT chk_fareobs_total_stops
        CHECK (total_stops >= 0),
    CONSTRAINT chk_fareobs_price
        CHECK (price >= 0)
);

-- Indexes for the app queries.
CREATE INDEX idx_route_source_dest ON Route(source_id, destination_id);
CREATE INDEX idx_fare_route ON Fare(route_id);
CREATE INDEX idx_fare_airline ON Fare(airline_id);
CREATE INDEX idx_fareobs_fare ON FareObs(fare_id);
CREATE INDEX idx_fareobs_journey_date ON FareObs(journey_date);

COMMIT;
