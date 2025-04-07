-- Test SELECT operations

-- Verify admin user was inserted
SELECT * FROM users WHERE id = '36c9050e-ddd3-4c3b-9731-9f487208bbc1';

-- Verify amenities were inserted
SELECT * FROM amenities;

-- Test INSERT operations

-- Insert a test user
INSERT INTO users (id, first_name, last_name, email, password)
VALUES (
    'a1b2c3d4-e5f6-47a8-9b0c-1d2e3f4a5b6c',
    'Test',
    'User',
    'test@example.com',
    '$2b$12$aaBbCcDdEeFfGgHhIiJjKk123456789ABCDEFGHIJKLMNOPQRSTUV' -- Example hash
);

-- Insert a test place
INSERT INTO places (id, title, description, price, latitude, longitude, owner_id)
VALUES (
    'b2c3d4e5-f6a7-48b9-0c1d-2e3f4a5b6c7d',
    'Test Place',
    'A beautiful place for testing',
    100.50,
    40.7128,
    -74.0060,
    'a1b2c3d4-e5f6-47a8-9b0c-1d2e3f4a5b6c'
);

-- Insert a test review
INSERT INTO reviews (id, text, rating, user_id, place_id)
VALUES (
    'c3d4e5f6-a7b8-49c0-1d2e-3f4a5b6c7d8e',
    'Great place!',
    5,
    'a1b2c3d4-e5f6-47a8-9b0c-1d2e3f4a5b6c',
    'b2c3d4e5-f6a7-48b9-0c1d-2e3f4a5b6c7d'
);

-- Associate amenities with place
INSERT INTO place_amenity (place_id, amenity_id)
VALUES 
    ('b2c3d4e5-f6a7-48b9-0c1d-2e3f4a5b6c7d', 'd4b45022-d76e-4c5e-bfd0-f4a34fa433e3'), -- WiFi
    ('b2c3d4e5-f6a7-48b9-0c1d-2e3f4a5b6c7d', 'f1b6ae8c-d9c7-4c33-8b91-d57a11b2825d'); -- Air Conditioning

-- Test SELECT for relationships

-- Get places owned by a user
SELECT p.* FROM places p WHERE p.owner_id = 'a1b2c3d4-e5f6-47a8-9b0c-1d2e3f4a5b6c';

-- Get reviews for a place
SELECT r.* FROM reviews r WHERE r.place_id = 'b2c3d4e5-f6a7-48b9-0c1d-2e3f4a5b6c7d';

-- Get amenities for a place
SELECT a.* FROM amenities a
JOIN place_amenity pa ON a.id = pa.amenity_id
WHERE pa.place_id = 'b2c3d4e5-f6a7-48b9-0c1d-2e3f4a5b6c7d';

-- Test UPDATE operations

-- Update user's email
UPDATE users
SET email = 'updated@example.com'
WHERE id = 'a1b2c3d4-e5f6-47a8-9b0c-1d2e3f4a5b6c';

-- Verify the update
SELECT * FROM users WHERE id = 'a1b2c3d4-e5f6-47a8-9b0c-1d2e3f4a5b6c';

-- Update place price
UPDATE places
SET price = 120.75
WHERE id = 'b2c3d4e5-f6a7-48b9-0c1d-2e3f4a5b6c7d';

-- Verify the update
SELECT * FROM places WHERE id = 'b2c3d4e5-f6a7-48b9-0c1d-2e3f4a5b6c7d';

-- Test DELETE operations

-- Remove amenity association
DELETE FROM place_amenity 
WHERE place_id = 'b2c3d4e5-f6a7-48b9-0c1d-2e3f4a5b6c7d' 
AND amenity_id = 'f1b6ae8c-d9c7-4c33-8b91-d57a11b2825d';

-- Verify the delete
SELECT * FROM place_amenity WHERE place_id = 'b2c3d4e5-f6a7-48b9-0c1d-2e3f4a5b6c7d';

-- Test constraint: attempt to insert duplicate review for same user/place (should fail)
INSERT INTO reviews (id, text, rating, user_id, place_id)
VALUES (
    'd4e5f6a7-b8c9-40d1-2e3f-4a5b6c7d8e9f',
    'Another review that should fail!',
    3,
    'a1b2c3d4-e5f6-47a8-9b0c-1d2e3f4a5b6c',
    'b2c3d4e5-f6a7-48b9-0c1d-2e3f4a5b6c7d'
);

-- Clean up test data (uncomment to execute)
/*
DELETE FROM place_amenity WHERE place_id = 'b2c3d4e5-f6a7-48b9-0c1d-2e3f4a5b6c7d';
DELETE FROM reviews WHERE id = 'c3d4e5f6-a7b8-49c0-1d2e-3f4a5b6c7d8e';
DELETE FROM places WHERE id = 'b2c3d4e5-f6a7-48b9-0c1d-2e3f4a5b6c7d';
DELETE FROM users WHERE id = 'a1b2c3d4-e5f6-47a8-9b0c-1d2e3f4a5b6c';
*/
