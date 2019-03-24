CREATE TABLE amount
(
    amount_id serial NOT NULL,
    amount numeric DEFAULT 100,
    CONSTRAINT amount_bigger_than_0 CHECK (amount >= 0),
    CONSTRAINT amount_pkey PRIMARY KEY (amount_id)
);

INSERT INTO amount VALUES (1, 100)