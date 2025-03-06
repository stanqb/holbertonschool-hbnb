# HBnB - Holberton BnB Project

## Overview
HBnB (Holberton BnB) is a comprehensive web application project that follows the architectural patterns of Airbnb. This project focuses on building a robust, scalable platform that allows users to list properties, manage amenities, leave reviews, and perform various administrative functions.

## Project Structure
The project is divided into two main parts:

1. **Part 1: Technical Documentation**
   - Architecture design and planning
   - UML diagrams (package, class, sequence)
   - System blueprint documentation
   
2. **Part 2: Implementation**
   - Business logic layer development
   - API endpoints creation
   - Data management
   - Testing and validation

## Part 1: Technical Documentation

### Objective
Create comprehensive technical documentation that serves as the foundation for developing the HBnB Evolution application. This documentation includes architectural diagrams, detailed class designs, and sequence flows to guide the implementation.

### Key Components

#### High-Level Package Diagram
- Three-layer architecture representation:
  - Presentation Layer: Services and API
  - Business Logic Layer: Core models
  - Persistence Layer: Database interactions
- Facade pattern implementation for layer communication

#### Detailed Class Diagram
- Business Logic entities (User, Place, Review, Amenity)
- Entity attributes and methods
- Inter-entity relationships
- Data validation and constraints

#### Sequence Diagrams
- User Registration flow
- Place Creation process
- Review Submission logic
- Fetching Places data flow

### Business Rules

#### User Entity
- Personal information (first name, last name, email, password)
- Administrator identification
- CRUD operations

#### Place Entity
- Property details (title, description, price, location)
- Owner association
- Amenities integration
- CRUD operations

#### Review Entity
- Association with places and users
- Rating and comment functionality
- CRUD operations

#### Amenity Entity
- Name and description attributes
- CRUD operations
- Association with places

## Part 2: Implementation

### Objective
Build the Presentation and Business Logic layers of the application using Python and Flask, based on the architectural design from Part 1.

### Key Components

#### Project Setup
- Organized modular structure
- Initialization of necessary packages
- Setup for layered architecture
- Implementation of the in-memory repository (temporary solution before database integration)

#### Business Logic Classes
- Implementation of core entities (User, Place, Review, Amenity)
- Entity relationships
- Data validation logic
- UUID implementation for unique identification

#### API Endpoints

##### User Management
- Create user (POST /api/v1/users/)
- Retrieve users (GET /api/v1/users/)
- Get user by ID (GET /api/v1/users/{user_id})
- Update user (PUT /api/v1/users/{user_id})

##### Amenity Management
- Create amenity (POST /api/v1/amenities/)
- Retrieve amenities (GET /api/v1/amenities/)
- Get amenity by ID (GET /api/v1/amenities/{amenity_id})
- Update amenity (PUT /api/v1/amenities/{amenity_id})

##### Place Management
- Create place (POST /api/v1/places/)
- Retrieve places (GET /api/v1/places/)
- Get place by ID (GET /api/v1/places/{place_id})
- Update place (PUT /api/v1/places/{place_id})

##### Review Management
- Create review (POST /api/v1/reviews/)
- Retrieve reviews (GET /api/v1/reviews/)
- Get review by ID (GET /api/v1/reviews/{review_id})
- Update review (PUT /api/v1/reviews/{review_id})
- Delete review (DELETE /api/v1/reviews/{review_id})

### Testing and Validation
- Input validation implementation
- API testing using cURL
- Swagger documentation
- Unit testing with unittest/pytest

## Technologies Used
- Python
- Flask framework
- Flask-RESTx for API development
- UML for system design
- JSON for data exchange
- UUID for unique identifiers

## Future Extensions
- Database integration using SQLAlchemy (Part 3)
- JWT authentication
- Role-based access control
- Enhanced search functionality
- User interface development

## Installation and Setup

### Requirements
- Python 3.8+
- Flask
- Flask-RESTx
- Other dependencies listed in requirements.txt

### Setup Instructions
1. Clone the repository
   ```
   git clone https://github.com/yourusername/holbertonschool-hbnb.git
   ```

2. Navigate to the project directory
   ```
   cd holbertonschool-hbnb
   ```

3. Install dependencies
   ```
   pip install -r requirements.txt
   ```

4. Run the application
   ```
   python3 app.py
   ```

5. Access the API documentation
   ```
   http://localhost:5000/api/v1/
   ```

## Author

- Stan QUEUNIEZ - [Holberton School](https://www.holbertonschool.com)
- Killian LEMOINE - [Holberton School](https://www.holbertonschool.com)
