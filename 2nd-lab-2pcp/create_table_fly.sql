CREATE TABLE fly_booking
(
  fly_id serial NOT NULL,
  client_name character varying(80),
  fly_number character varying(80),
  fly_from character varying(80),
  fly_to character varying(80),
  book_date date
  CONSTRAINT fly_booking_pkey PRIMARY KEY (fly_id)
);