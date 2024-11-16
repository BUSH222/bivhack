-- USERS AND RELATED
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(32) UNIQUE,
    password VARCHAR(32), 
    isAdmin BOOLEAN,
);

CREATE TABLE IF NOT EXISTS insurance_product (
    id SERIAL PRIMARY KEY,
    field_id INTEGER UNIQUE,
);

CREATE TABLE IF NOT EXISTS insurance_product_info (
    id SERIAL PRIMARY KEY,
    description INTEGER UNIQUE,
);

