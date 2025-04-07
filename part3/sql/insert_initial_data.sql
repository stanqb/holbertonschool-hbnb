-- Insert Administrator User
-- Password: admin1234 hashed with bcrypt
INSERT INTO users (id, first_name, last_name, email, password, is_admin)
VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    'Admin',
    'HBnB',
    'admin@hbnb.io',
    '$2b$12$ZVw1rRdIXVJdU7.8iJl8Fe3qVhm8w4hj8/Ib5EVrOFZ3Wc63EQnH2', -- bcrypt hash of 'admin1234'
    TRUE
);

-- Insert Initial Amenities
INSERT INTO amenities (id, name)
VALUES 
    ('d4b45022-d76e-4c5e-bfd0-f4a34fa433e3', 'WiFi'),
    ('e81305a2-7fa0-4b82-b4ad-c3cf2e0ae9f1', 'Swimming Pool'),
    ('f1b6ae8c-d9c7-4c33-8b91-d57a11b2825d', 'Air Conditioning');
