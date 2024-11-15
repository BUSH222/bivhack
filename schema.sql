-- USERS AND RELATED
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(32) UNIQUE,
    email VARCHAR(32) UNIQUE,
    password VARCHAR(32), 
    profile_pic TEXT,
    role VARCHAR(2), -- role numbers a user has, ascending. user-0; admin-1;
);