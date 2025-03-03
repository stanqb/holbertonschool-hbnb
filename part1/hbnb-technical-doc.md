# HBnB - UML Technical Documentation HOLBERTON SCHOOL
Version 1.0

## 1) Introduction
The HBnB Evolution application is a housing booking platform inspired by AirBnB. It allows users to manage locations, reserve properties, submit reviews and manage amenities. This documentation describes in detail the architecture, business entities, interaction flows and management rules.

## 2) High Level Architecture:

### 2.1) Package Diagram:

![HBnB Package Diagram](./images/package-diagram.png)

Layers:

1. Presentation:
   Responsibility: Manage user interactions via REST APIs.
   Components:
   - UserService: Manages user registration, login and updates.
   - PlaceService: Manages creation, modification and deletion of places.
   - ReviewService: Manages submission and management of reviews.
   - AmenityService: Manages amenities associated with places.

2. Business Logic:
   Responsibility: Implement business rules and manage entities.
   Components:
   - UserManager: Manages users (creation, update, deletion).
   - PlaceManager: Manages places and their relationships with users and amenities.
   - ReviewManager: Manages reviews and their relationships with places and users.
   - AmenityManager: Manages available amenities for places.

3. Persistence:
   Responsibility: Store and retrieve data in a database.
   Components:
   - UserRepository: Access to user data.
   - PlaceRepository: Access to place data.
   - ReviewRepository: Access to review data.
   - AmenityRepository: Access to amenity data.

Facade Pattern:
Layers communicate through simplified interfaces (e.g., PlaceFacade for place management). This allows for layer decoupling and easier testing.

## 3) Class Diagram (Business Logic):

![HBnB Class Diagram](./images/class_diagram.png)

### 3.1) Main Entities:

Classes:

1) User:
   Relations:
   - A User can own multiple Places (1..n).
   - A User can submit multiple Reviews (1..n).

2) Place:
   Relations:
   - A Place can have multiple Amenities (1..n).
   - A Place can have multiple Reviews (1..n).

3) Amenity:
   Relations:
   - An Amenity can be associated with multiple Places (n..n).

4) Review:
   Relations:
   - A Review is associated with one User and one Place.

## 4) API Call Flows:

### 4.1) Creating a Place:

![HBnB Creating a Place](./images/place_creation.png)

Sequence:
1. User sends place data via API (POST /places).
2. Presentation layer validates data (e.g., non-empty title, price > 0).
3. Business Logic layer verifies business rules (e.g., user exists).
4. Persistence layer saves the place in the database.
5. A response is sent back to the user (success or error).

### 4.2) Submitting a Review:

![HBnB Review Submission](./images/review_submission.png)

Sequence:
1. User sends a review via API (POST /reviews).
2. Rating validation (1-5 stars).
3. Storage in database via ReviewRepository.
4. A response is sent back to the user (success or error).

### 4.3) Fetching a list of Places:

![HBnB Fetching a list of Places](./images/fetching_a_list_of_places.png)

Sequence:
1. User requests a list of places via API (GET /places).
2. Presentation layer applies search criteria (e.g., maximum price, location).
3. Business Logic layer queries the database via PlaceRepository.
4. List of places is returned to the user or an error is generated.

### 4.4) User Registration:

![HBnB User Registration](./images/user_registration.png)

Sequence:
1. User sends their information via API (POST /users).
2. Presentation layer validates data (e.g., valid email, strong password).
3. Business Logic layer verifies email uniqueness.
4. Persistence layer saves the user in the database.
5. A response is sent back to the user (success or error).

## 5) Business Rules

### 5.1) User
- A user must have a unique email.
- An administrator can modify/delete any place or review.

### 5.2) Place
- A place must have a title, description and price.
- Geographic coordinates (latitude, longitude) are mandatory.

### 5.3) Review
- A user can only submit one review per place.
- The rating must be between 1 and 5.
