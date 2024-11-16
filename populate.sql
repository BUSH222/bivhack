INSERT INTO users (name, password, is_admin) VALUES
('alice', 'password1', FALSE),   -- Admin user
('bob', 'securepass123', TRUE),   -- Regular user
('charlie', 'password2', FALSE);

INSERT INTO insurance_products (name, description) VALUES
('Car Insurance', 'Comprehensive insurance for vehicles'),
('Home Insurance', 'Insurance for your home and property'),
('Health Insurance', 'Coverage for medical expenses');

INSERT INTO fields (var_name, description, variable_type, variable_formula, default_value, hidden, editable) VALUES
('owner_name', 'Name of the owner', 0, NULL, '"Default Owner"', FALSE, TRUE),  -- String type
('car_vin', 'Vehicle Identification Number', 0, NULL, NULL, FALSE, TRUE),     -- String type
('property_value', 'Estimated value of property', 1, NULL, '100000', FALSE, TRUE), -- Number
('medical_history', 'Medical history required', 2, NULL, 'false', FALSE, TRUE);    -- Boolean

INSERT INTO insurance_product_fields (insurance_product_id, field_id) VALUES
(1, 1), -- Car Insurance -> owner_name
(1, 2), -- Car Insurance -> car_vin
(2, 1), -- Home Insurance -> owner_name
(2, 3), -- Home Insurance -> property_value
(3, 1), -- Health Insurance -> owner_name
(3, 4); -- Health Insurance -> medical_history

INSERT INTO insurance_product_categories (name, description) VALUES
('Vehicle', 'Insurance for all types of vehicles'),
('Property', 'Insurance for homes, buildings, and land'),
('Health', 'Insurance for medical expenses and health coverage');

INSERT INTO insurance_product_categories_connections (insurance_product_category_id, insurance_product_id) VALUES
(1, 1), -- Vehicle -> Car Insurance
(2, 2), -- Property -> Home Insurance
(3, 3); -- Health -> Health Insurance

INSERT INTO contracts (user_id, insurance_product_id, insurance_product_data) VALUES
(2, 1, '{"owner_name": "Bob", "car_vin": "1HGCM82633A123456"}', TRUE), -- Bob's car insurance contract
(3, 2, '{"owner_name": "Charlie", "property_value": 200000}'),   -- Charlie's home insurance contract
(2, 3, '{"owner_name": "Bob", "medical_history": true}');        -- Bob's health insurance contract
