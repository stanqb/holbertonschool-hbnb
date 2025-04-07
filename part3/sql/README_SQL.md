# SQL Scripts for HBnB Database

This directory contains SQL scripts to create the database schema for the HBnB project and insert initial data.

## Files

- `create_tables.sql`: Creates all the tables with proper relationships
- `insert_initial_data.sql`: Inserts the administrator user and initial amenities
- `test_crud_operations.sql`: Tests CRUD operations on the database
- `generate_uuid.py`: Utility script to generate UUID4 values

## How to Use

### Create the tables

```bash
mysql -u your_username -p your_database_name < create_tables.sql
```

### Insert initial data

```bash
mysql -u your_username -p your_database_name < insert_initial_data.sql
```

### Test CRUD operations

```bash
mysql -u your_username -p your_database_name < test_crud_operations.sql
```

### Generate UUIDs (if needed)

```bash
python generate_uuid.py
```

## Database Structure

### Tables

1. **users**
   - `id`: CHAR(36) PRIMARY KEY (UUID format)
   - `first_name`: VARCHAR(255)
   - `last_name`: VARCHAR(255)
   - `email`: VARCHAR(255) UNIQUE
   - `password`: VARCHAR(255) (Bcrypt hashed)
   - `is_admin`: BOOLEAN DEFAULT FALSE
   - `created_at`: TIMESTAMP
   - `updated_at`: TIMESTAMP

2. **places**
   - `id`: CHAR(36) PRIMARY KEY (UUID format)
   - `title`: VARCHAR(255)
   - `description`: TEXT
   - `price`: DECIMAL(10, 2)
   - `latitude`: FLOAT
   - `longitude`: FLOAT
   - `owner_id`: CHAR(36) (Foreign key to users.id)
   - `created_at`: TIMESTAMP
   - `updated_at`: TIMESTAMP

3. **reviews**
   - `id`: CHAR(36) PRIMARY KEY (UUID format)
   - `text`: TEXT
   - `rating`: INT (1-5)
   - `user_id`: CHAR(36) (Foreign key to users.id)
   - `place_id`: CHAR(36) (Foreign key to places.id)
   - `created_at`: TIMESTAMP
   - `updated_at`: TIMESTAMP
   - Unique constraint on (user_id, place_id)

4. **amenities**
   - `id`: CHAR(36) PRIMARY KEY (UUID format)
   - `name`: VARCHAR(255) UNIQUE
   - `created_at`: TIMESTAMP
   - `updated_at`: TIMESTAMP

5. **place_amenity** (Junction table for many-to-many)
   - `place_id`: CHAR(36) (Foreign key to places.id)
   - `amenity_id`: CHAR(36) (Foreign key to amenities.id)
   - Composite PRIMARY KEY (place_id, amenity_id)

## Relationships

- User has many Places (one-to-many)
- Place has many Reviews (one-to-many)
- User has many Reviews (one-to-many)
- Place and Amenity have a many-to-many relationship through place_amenity
