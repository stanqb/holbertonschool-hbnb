# HBnB Implementation Phase

## Overview
This project implements the business logic and API endpoints for the HBnB (Holberton BnB) application, an Airbnb-like platform. The implementation follows the architectural design created in the documentation phase, focusing on Python and Flask to build a RESTful API.

## Scope
This phase focuses on implementing:
- The core business logic classes
- RESTful API endpoints for CRUD operations
- Data serialization and relationship handling
- Basic validation and testing

Authentication and database integration will be addressed in future phases.

## Project Structure
The implementation follows a three-layer architecture:
- **Presentation Layer**: API endpoints built with Flask and flask-restx
- **Business Logic Layer**: Core entity classes and business rules
- **Persistence Layer**: In-memory repository (temporary solution)

## Core Features

### Business Logic Classes
- **User**: Personal information management (name, email, password)
- **Place**: Property listing data (title, description, price, location)
- **Review**: User feedback on properties (rating, comments)
- **Amenity**: Features available at properties

### API Endpoints

#### User Management
- `POST /api/v1/users/`: Create a new user
- `GET /api/v1/users/`: Retrieve all users
- `GET /api/v1/users/{id}`: Retrieve a specific user
- `PUT /api/v1/users/{id}`: Update user information

#### Amenity Management
- `POST /api/v1/amenities/`: Create a new amenity
- `GET /api/v1/amenities/`: Retrieve all amenities
- `GET /api/v1/amenities/{id}`: Retrieve a specific amenity
- `PUT /api/v1/amenities/{id}`: Update amenity information

#### Place Management
- `POST /api/v1/places/`: Create a new place
- `GET /api/v1/places/`: Retrieve all places
- `GET /api/v1/places/{id}`: Retrieve a specific place
- `PUT /api/v1/places/{id}`: Update place information

#### Review Management
- `POST /api/v1/reviews/`: Create a new review
- `GET /api/v1/reviews/`: Retrieve all reviews
- `GET /api/v1/reviews/{id}`: Retrieve a specific review
- `PUT /api/v1/reviews/{id}`: Update review information
- `DELETE /api/v1/reviews/{id}`: Delete a review

## Implementation Features
- **Facade Pattern**: Simplifies communication between layers
- **Data Validation**: Ensures data integrity and correctness
- **Relationship Handling**: Manages relationships between entities
- **API Documentation**: Automatic Swagger documentation via flask-restx
- **Modular Design**: Ensures code maintainability and scalability

## Technologies Used
- Python
- Flask web framework
- flask-restx for API development
- UUID for unique identifiers
- JSON for data serialization
- In-memory storage (temporary)

## Installation and Setup
1. Clone the repository
   ```
   git clone https://github.com/yourusername/holbertonschool-hbnb.git
   ```

2. Navigate to the project directory
   ```
   cd holbertonschool-hbnb/part2
   ```

3. Install dependencies
   ```
   pip install -r requirements.txt
   ```

4. Run the application
   ```
   python run.py
   ```

5. Access the API documentation
   ```
   http://localhost:5000/api/v1/
   ```

## Testing
- API endpoints can be tested using cURL or Postman
- Swagger UI provides interactive testing capability
- Basic validation ensures data integrity

## Future Enhancements
- Database integration with SQLAlchemy
- JWT authentication
- Role-based access control
- Enhanced validation
- Comprehensive unit and integration testing

## Authors

- Stan QUEUNIEZ - [Holberton School](https://www.holbertonschool.com)
- Killian LEMOINE - [Holberton School](https://www.holbertonschool.com)

