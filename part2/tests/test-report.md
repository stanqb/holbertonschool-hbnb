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
| Create Valid Place | Valid place data | 201 Created with place data | 404 Not Found | ❌ FAIL |
| Create Place with Invalid Latitude | Latitude > 90 | 400 Bad Request with error message | 404 Not Found | ❌ FAIL |
| Create Place with Negative Price | Price < 0 | 400 Bad Request with error message | 404 Not Found | ❌ FAIL |
| Get Place by ID | Valid place ID | 200 OK with place data | 404 Not Found | ❌ FAIL |

### Review Endpoints

| Test Case | Input | Expected Output | Actual Output | Status |
|-----------|-------|-----------------|---------------|--------|
| Create Valid Review | Valid review data | 201 Created with review data | 400 Bad Request with validation errors | ⚠️ PARTIAL |
| Create Review with Empty Text | Text is empty | 400 Bad Request with error message | 400 Bad Request with validation errors | ✅ PASS |
| Create Review with Invalid Rating | Rating > 5 | 400 Bad Request with error message | 400 Bad Request with validation errors | ✅ PASS |
| Get Review by ID | Valid review ID | 200 OK with review data | 200 OK (empty list) | ⚠️ PARTIAL |
| Get Reviews by Place | Valid place ID | 200 OK with reviews data | 404 Not Found | ❌ FAIL |

### Amenity Endpoints

| Test Case | Input | Expected Output | Actual Output | Status |
|-----------|-------|-----------------|---------------|--------|
| Create Valid Amenity | `{"name": "WiFi"}` | 201 Created with amenity data | 201 Created with amenity data | ✅ PASS |
| Create Amenity with Empty Name | `{"name": ""}` | 400 Bad Request with error message | 400 Bad Request with error details | ✅ PASS |
| Get Amenity by ID | Valid amenity ID | 200 OK with amenity data | 200 OK with amenity data (list) | ✅ PASS |

## Issues Identified

1. **Place Endpoints Not Accessible**
   - All place-related endpoints return 404 Not Found
   - Possible causes: routing issues, namespace registration problems, or implementation errors

2. **Review Creation Partially Working**
   - Validation works correctly (empty text, invalid rating)
   - But fails with place and user IDs, indicating potential reference validation issues

3. **Amenity Name Validation Implemented**
   - Previously, empty amenity names were accepted but should be rejected
   - Implementation has been successfully corrected to validate amenity names

4. **Reviews by Place Route Not Found**
   - The endpoint for getting reviews by place is not accessible
   - Route may be incorrectly defined or may need path adjustments

## Improvements Made

1. **Added User Validation**
   - Implemented validation for first_name, last_name, and email format
   - Validation prevents creation of users with empty names or invalid emails

2. **Added Review Validation**
   - Implemented validation for text content, rating range, and reference IDs
   - Validation prevents creation of reviews with empty text or invalid ratings

3. **Added Amenity Name Validation**
   - Implemented validation to prevent empty amenity names
   - Updated both POST and PUT endpoints to include validation

## Swagger Documentation

The API includes Swagger documentation accessible at http://127.0.0.1:5000/. The documentation automatically displays all endpoints, expected request formats, and response codes.

## Conclusion

The testing process has successfully identified several issues with the API implementation:

1. **Working Endpoints**: User endpoints and Amenity endpoints are fully functional with proper validation
2. **Partially Working**: Review endpoints have validation but reference issues
3. **Not Working**: Place endpoints are not accessible

To make the API fully functional, the following actions are recommended:

1. Debug and fix the Place endpoints routing/implementation
2. Ensure correct reference validation for Reviews
3. Fix the route for getting reviews by place
4. Complete the implementation of validation for all entities

These improvements will ensure that the API meets all the requirements specified in the task.

## Testing Process

The testing process followed these steps:

1. **Implementation of Validations**: Added validation methods to each model class to verify data integrity.
2. **Creation of Test Script**: Developed the test_api.sh script to automate testing of all endpoints.
3. **Manual Testing**: Executed the test script against the running API server.
4. **Analysis of Results**: Examined the responses to identify successful and failed tests.
5. **Corrections**: Made necessary adjustments to the validation logic based on test results.
6. **Retesting**: Ran the tests again to verify that corrections were effective.

## Next Steps

1. Fix the identified issues with Place and Review endpoints
2. Implement unit tests using Python's unittest framework
3. Complete end-to-end testing after all fixes
4. Update Swagger documentation as needed

## Authors

- Stan QUEUNIEZ
- Killian LEMOINE
