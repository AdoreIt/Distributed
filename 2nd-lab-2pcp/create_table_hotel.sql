CREATE TABLE hotel_booking
(
  hotel_id serial NOT NULL,
  client_name character varying(80),
  hotel_name character varying(80),
  arrival_date date,
  departure_date date,
  CONSTRAINT hotel_booking_pkey PRIMARY KEY (hotel_id)
);