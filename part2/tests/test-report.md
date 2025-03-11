# HBNB API Testing Report

## Introduction

This report documents the testing process and results for the HBNB API. The testing focused on validating the API endpoints and ensuring that proper data validation is implemented at the model level. The tests were performed using cURL commands to simulate HTTP requests to the API.

## Test Environment

- **Server**: Flask development server
- **Host**: http://127.0.0.1:5000
- **API Base URL**: http://127.0.0.1:5000/api/v1
- **Testing Tool**: cURL via Bash script (test_api.sh)
- **Testing Date**: March 11, 2025

### Project Structure
The tests were performed on the HBNB project with the following structure:

```
hbnb/
├── app/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── v1/
│   │       ├── __init__.py
│   │       ├── users.py
│   │       ├── places.py
│   │       ├── reviews.py
│   │       ├── amenities.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── place.py
│   │   ├── review.py
│   │   ├── amenity.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── facade.py
│   ├── persistence/
│       ├── __init__.py
│       ├── repository.py
├── run.py
├── config.py
├── requirements.txt
├── README.md
├── test_api.sh
```

### Files Used for Testing
- **test_api.sh**: Bash script containing cURL commands to test all API endpoints
- **run.py**: Entry point to start the Flask server
- **app/api/v1/users.py, places.py, reviews.py, amenities.py**: API endpoint implementations that were tested
- **app/models/user.py, place.py, review.py, amenity.py**: Model files where validations were implemented

## Validation Implementation

Basic validation was implemented for all entity models as requested in the task:

### User Validation
- First name and last name cannot be empty
- Email must be in valid format (using regex pattern)

### Place Validation
- Title cannot be empty and must be less than 100 characters
- Price must be a positive number
- Latitude must be between -90 and 90
- Longitude must be between -180 and 180
- Owner ID must be valid

### Review Validation
- Text cannot be empty
- Rating must be between 1 and 5
- User ID and Place ID must be valid

### Amenity Validation
- Name cannot be empty

## Test Results

### User Endpoints

| Test Case | Input | Expected Output | Actual Output | Status |
|-----------|-------|-----------------|---------------|--------|
| Create Valid User | `{"first_name": "John", "last_name": "Doe", "email": "john.doe@example.com"}` | 201 Created with user data | 201 Created with user data | ✅ PASS |
| Create User with Invalid Email | `{"first_name": "Jane", "last_name": "Doe", "email": "invalid-email"}` | 400 Bad Request with error message | 400 Bad Request with error details | ✅ PASS |
| Create User with Empty First Name | `{"first_name": "", "last_name": "Doe", "email": "jane.doe@example.com"}` | 400 Bad Request with error message | 400 Bad Request with error details | ✅ PASS |
| Get User by ID | Valid user ID | 200 OK with user data | 200 OK with user data | ✅ PASS |

### Place Endpoints

| Test Case | Input | Expected Output | Actual Output | Status |
|-----------|-------|-----------------|---------------|--------|
| Create Valid Place | Valid place data | 201 Created with place data | 201 Created with place data | ✅ PASS |
| Create Place with Invalid Latitude | Latitude > 90 | 400 Bad Request with error message | 400 Bad Request with error details | ✅ PASS |
| Create Place with Negative Price | Price < 0 | 400 Bad Request with error message | 400 Bad Request with error details | ✅ PASS |
| Get Place by ID | Valid place ID | 200 OK with place data | 200 OK with place data | ✅ PASS |

### Review Endpoints

| Test Case | Input | Expected Output | Actual Output | Status |
|-----------|-------|-----------------|---------------|--------|
| Create Valid Review | Valid review data | 201 Created with review data | 201 Created with review data | ✅ PASS |
| Create Review with Empty Text | Text is empty | 400 Bad Request with error message | 400 Bad Request with validation errors | ✅ PASS |
| Create Review with Invalid Rating | Rating > 5 | 400 Bad Request with error message | 400 Bad Request with validation errors | ✅ PASS |
| Get Review by ID | Valid review ID | 200 OK with review data | 200 OK with review data | ✅ PASS |
| Get Reviews by Place | Valid place ID | 200 OK with reviews data | 200 OK with reviews data | ✅ PASS |

### Amenity Endpoints

| Test Case | Input | Expected Output | Actual Output | Status |
|-----------|-------|-----------------|---------------|--------|
| Create Valid Amenity | `{"name": "WiFi"}` | 201 Created with amenity data | 201 Created with amenity data | ✅ PASS |
| Create Amenity with Empty Name | `{"name": ""}` | 400 Bad Request with error message | 400 Bad Request with error details | ✅ PASS |
| Get Amenity by ID | Valid amenity ID | 200 OK with amenity data | 200 OK with amenity data | ✅ PASS |

## Issues and Solutions Implemented

### Initial Issues

1. **Place Endpoints Not Accessible**
   - Issue: All place-related endpoints returned 404 Not Found
   - Solution: Modified the route definition in `places.py` from `@api.route('')` to `@api.route('/')` to correctly handle the routes

2. **ID Extraction Problems**
   - Issue: The script was unable to extract IDs from responses correctly
   - Solution: Improved the ID extraction method in the test script using a more robust approach with sed and text processing

3. **Reviews by Place Route Not Found**
   - Issue: The endpoint for getting reviews by place was not accessible
   - Solution: Fixed the route path in the test script to match the implementation in the API

### Debugging Process

1. **Examining API Responses**
   - Used detailed logging to track HTTP responses and error messages
   - Identified that most errors were related to routing and data extraction

2. **Route Analysis**
   - Analyzed the Flask route definitions and identified mismatches between expected and actual routes
   - Found that empty string routes (`''`) weren't correctly handled by Flask-RESTX compared to explicit routes (`'/'`)

3. **Tracing Request Paths**
   - Used server logs to trace each request path
   - Identified the correct endpoint structure for reviews by place

## Improvements Made

1. **Route Definitions Fixed**
   - Updated route definitions to use explicit paths
   - Ensured consistent route naming across the API

2. **Test Script Enhancement**
   - Improved ID extraction logic for better robustness
   - Updated route calls to match the actual API implementation

3. **Request/Response Verification**
   - Added better error handling to the test script
   - Enhanced output formatting for better readability

## Swagger Documentation

The API includes Swagger documentation accessible at http://127.0.0.1:5000/. The documentation automatically displays all endpoints, expected request formats, and response codes.

## Conclusion

After applying the fixes, all API endpoints now function correctly with proper validation:

1. **User Endpoints**: Function fully with proper validation for email format and required fields
2. **Place Endpoints**: Now accessible and properly validating latitude, longitude, price, and required fields
3. **Review Endpoints**: Functioning correctly with proper validation of rating ranges and content requirements
4. **Amenity Endpoints**: Working correctly with validation for required fields

The API now meets all the requirements specified in the task. The testing process successfully identified issues and verified that they were resolved.

## Testing Process

The debugging and testing process followed these steps:

1. **Initial Testing**: Executed the original test script to identify failing endpoints
2. **Debugging Routes**: Examined API route definitions to identify mismatches
3. **Fixing Route Definitions**: Updated route paths in `places.py` and other modules
4. **Enhancing Test Script**: Improved ID extraction and route paths in the test script
5. **Retesting**: Verified that all endpoints now work as expected
6. **Documentation**: Updated test report to reflect current status

## Next Steps

1. Add more comprehensive tests for edge cases
2. Implement unit tests using Python's unittest or pytest framework
3. Consider adding authentication and authorization tests
4. Enhance documentation with more detailed examples

## Authors

- Stan QUEUNIEZ
- Killian LEMOINE