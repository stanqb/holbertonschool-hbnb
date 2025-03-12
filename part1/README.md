# HBnB Technical Documentation

## Overview
This project focuses on creating comprehensive technical documentation for the HBnB (Holberton BnB) application, an Airbnb-like platform. The documentation serves as the architectural foundation for the subsequent implementation phases.

## Project Scope
The documentation covers the design and architecture of a platform that enables:
- User management (registration, profile updates)
- Property listings management
- Review submission and management
- Amenity management for properties

## Components

### High-Level Package Diagram
- Illustrates the three-layer architecture:
  - Presentation Layer (API/Services)
  - Business Logic Layer (Models)
  - Persistence Layer (Database)
- Shows communication between layers via facade pattern

### Detailed Class Diagram
- Represents the Business Logic Layer entities:
  - User (attributes, methods, relationships)
  - Place (attributes, methods, relationships)
  - Review (attributes, methods, relationships)
  - Amenity (attributes, methods, relationships)
- Includes entity relationships and data constraints

### Sequence Diagrams
- Visualizes the interaction flow for key API operations:
  - User Registration
  - Place Creation
  - Review Submission
  - Place Listing Retrieval

### Documentation Compilation
- Combines all diagrams and explanatory notes into a comprehensive reference document
- Provides clear guidance for implementation

## Business Rules

### Entity Requirements
- All entities have unique identifiers (UUID)
- Creation and update timestamps are recorded for all entities
- Specific validation rules applied to each entity type

### User Entity
- Contains personal information (name, email, password)
- Administrator role capability

### Place Entity
- Contains property details (title, description, price, location)
- Associated with owner (User)
- Can have multiple Amenities

### Review Entity
- Links User and Place entities
- Contains rating and comment data

### Amenity Entity
- Defines features that can be associated with Places

## Tools Used
- UML notation for all diagrams
- Mermaid.js for diagram creation
- Documentation follows industry standards

## Authors

- Stan QUEUNIEZ - [Holberton School](https://www.holbertonschool.com)
- Killian LEMOINE - [Holberton School](https://www.holbertonschool.com)

