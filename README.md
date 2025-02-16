# HBnB Project (AirBnB Clone)

## Project Overview

HBnB is an educational project that aims to create a simplified version of AirBnB. This project implements a complete web application integrating database storage, a back-end API, and front-end interface.

## Architecture

The application follows a layered architecture divided into three main components:

### 1. Front-end Layer
- **Home Page & Navigation**: Main interface and site navigation
- **User's Page**: User profile and management
- **Booking Page**: Reservation interface
- **Property Presentation**: Detailed view of properties
- **Notification Page**: User notifications system

### 2. Back-end Layer
- **Users Management**: Handles user operations and authentication
- **Booking Management**: Processes reservations and availability
- **Review Management**: Manages property reviews and ratings

### 3. Business Layer
The business layer is divided into three main components:

#### Booking Layer
- Availability checking
- Price calculation
- Inscription service

#### User Layer
- Authentication service
- Profile management
- User data operations

#### Property Layer
- Property management (add/remove)
- Property updates (prices, pictures, descriptions)

### 4. Data Layer
- Users Repository
- Code Repository
- Property Repository

### 5. Cross-cutting Concerns
- **Security**
  - Authentication management
  - Restricted access to data
- **Error Handling**
- **Communication**
  - Chat system (booker/renter)
  - Help system (user/staff)

## Key Features

1. **User Management**
   - User registration and authentication
   - Profile management
   - Admin/regular user roles

2. **Property Management**
   - Property listing creation and management
   - Amenity association
   - Location tracking (latitude/longitude)

3. **Booking System**
   - Availability checking
   - Price calculation
   - Reservation management

4. **Review System**
   - Property reviews
   - Rating system
   - Comment management

## Technical Specifications

### Data Models

1. **User**
   - First name
   - Last name
   - Email
   - Password
   - Admin status (boolean)
   - Created at
   - Updated at

2. **Place**
   - Title
   - Description
   - Price
   - Latitude
   - Longitude
   - Owner (User reference)
   - Amenities
   - Created at
   - Updated at

3. **Review**
   - Rating
   - Comment
   - User reference
   - Place reference
   - Created at
   - Updated at

4. **Amenity**
   - Name
   - Description
   - Created at
   - Updated at

### Technical Requirements

- All objects have unique identifiers (UUID4)
- Creation and update timestamps for all entities
- Secure password handling
- RESTful API implementation
- Database persistence

## Development Phases

1. **Phase 1: Technical Documentation**
   - Architecture design
   - Package diagrams
   - Class diagrams
   - Sequence diagrams

2. **Phase 2: Implementation**
   - Database setup
   - Back-end development
   - API implementation
   - Front-end development

3. **Phase 3: Testing**
   - Unit testing
   - Integration testing
   - User acceptance testing

## Contributing

This is an educational project. While it's not open for public contributions, feedback and suggestions are welcome.

## License

This project is part of the curriculum at Holberton School. All rights reserved.

## Authors

- Stan QUEUNIEZ
- Killian LEMOINE

## Acknowledgments

- This project is inspired by AirBnB
- Special thanks to our school and mentors

## Project Status

Currently in Phase 1: Technical Documentation
