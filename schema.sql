-- USERS AND RELATED
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(32) UNIQUE NOT NULL,
    password VARCHAR(128) NOT NULL, 
    is_admin BOOLEAN DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS fields (
    id SERIAL PRIMARY KEY,
    var_name VARCHAR(32) UNIQUE,
    description TEXT,
    variable_type SMALLINT, --  0: string, 1: number (int/float), 2: boolean
    variable_formula TEXT,
    default_value JSONB, -- Can store: string, int, float, bool
    hidden BOOLEAN DEFAULT FALSE,
    editable BOOLEAN DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS insurance_products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(32) NOT NULL UNIQUE,
    description TEXT,
    signable BOOLEAN DEFAULT TRUE,
);

CREATE TABLE IF NOT EXISTS insurance_product_fields (
    id SERIAL PRIMARY KEY,
    insurance_product_id INTEGER REFERENCES insurance_products(id) ON DELETE CASCADE,
    field_id INTEGER REFERENCES fields(id) ON DELETE CASCADE,
    UNIQUE (insurance_product_id, field_id)
);

CREATE TABLE IF NOT EXISTS insurance_product_categories(
    id SERIAL PRIMARY KEY,
    name VARCHAR(32) UNIQUE,
    description TEXT
);

CREATE TABLE IF NOT EXISTS insurance_product_categories_connections(
    id SERIAL PRIMARY KEY,
    insurance_product_category_id INTEGER REFERENCES insurance_product_categories(id) ON DELETE CASCADE,
    insurance_product_id INTEGER REFERENCES insurance_products(id) ON DELETE CASCADE,
    UNIQUE (insurance_product_category_id, insurance_product_id)
);

CREATE TABLE IF NOT EXISTS contracts (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    insurance_product_id INTEGER REFERENCES insurance_products(id) ON DELETE CASCADE,
    insurance_product_data JSONB, -- key-value pairs of fields and values
    signatures BYTEA,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


