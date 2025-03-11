#!/bin/bash
# API Testing Script for HBNB Project
# This script tests all the endpoints of the HBNB API

# Base URL for the API
API_URL="http://127.0.0.1:5000"

# Text colors for better readability
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}==== HBNB API Testing Script ====${NC}"
echo "Testing API at: $API_URL"
echo ""

# Function to print section headers
section() {
    echo -e "${YELLOW}==== Testing $1 ====${NC}"
}

# Function to print test headers
test_case() {
    echo -e "${YELLOW}=== Test: $1 ===${NC}"
}

# Store IDs for later use
USER_ID=""
PLACE_ID=""
REVIEW_ID=""
AMENITY_ID=""

# ====== USER TESTS ======
section "User Endpoints"

# Test: Create Valid User
test_case "Create Valid User"
USER_RESPONSE=$(curl -s -X POST "$API_URL/api/v1/users/" \
     -H "Content-Type: application/json" \
     -d '{
         "first_name": "John",
         "last_name": "Doe",
         "email": "john.doe@example.com"
     }')
echo "$USER_RESPONSE"

# Extract the user ID for later use
USER_ID=$(echo $USER_RESPONSE | grep -o '"id":"[^"]*' | cut -d'"' -f4)
echo -e "Extracted USER_ID: ${GREEN}$USER_ID${NC}"
echo ""

# Test: Create User with Invalid Email
test_case "Create User with Invalid Email"
curl -s -X POST "$API_URL/api/v1/users/" \
     -H "Content-Type: application/json" \
     -d '{
         "first_name": "Jane",
         "last_name": "Doe",
         "email": "invalid-email"
     }'
echo ""
echo ""

# Test: Create User with Empty First Name
test_case "Create User with Empty First Name"
curl -s -X POST "$API_URL/api/v1/users/" \
     -H "Content-Type: application/json" \
     -d '{
         "first_name": "",
         "last_name": "Doe",
         "email": "jane.doe@example.com"
     }'
echo ""
echo ""

# Test: Get User by ID
test_case "Get User by ID"
curl -s -X GET "$API_URL/api/v1/users/$USER_ID"
echo ""
echo ""

# ====== PLACE TESTS ======
section "Place Endpoints"

# Test: Create Valid Place
test_case "Create Valid Place"
PLACE_RESPONSE=$(curl -s -X POST "$API_URL/api/v1/places/" \
     -H "Content-Type: application/json" \
     -d '{
         "title": "Beautiful Apartment",
         "description": "A lovely apartment in the heart of the city",
         "price": 100.0,
         "latitude": 48.8566,
         "longitude": 2.3522,
         "owner_id": "'$USER_ID'"
     }')
echo "$PLACE_RESPONSE"

# Extract the place ID for later use
PLACE_ID=$(echo $PLACE_RESPONSE | grep -o '"id":"[^"]*' | cut -d'"' -f4)
echo -e "Extracted PLACE_ID: ${GREEN}$PLACE_ID${NC}"
echo ""

# Test: Create Place with Invalid Latitude
test_case "Create Place with Invalid Latitude"
curl -s -X POST "$API_URL/api/v1/places/" \
     -H "Content-Type: application/json" \
     -d '{
         "title": "Invalid Place",
         "description": "A place with invalid latitude",
         "price": 120.0,
         "latitude": 95.0,
         "longitude": 2.3522,
         "owner_id": "'$USER_ID'"
     }'
echo ""
echo ""

# Test: Create Place with Negative Price
test_case "Create Place with Negative Price"
curl -s -X POST "$API_URL/api/v1/places/" \
     -H "Content-Type: application/json" \
     -d '{
         "title": "Negative Price Place",
         "description": "A place with negative price",
         "price": -50.0,
         "latitude": 48.8566,
         "longitude": 2.3522,
         "owner_id": "'$USER_ID'"
     }'
echo ""
echo ""

# Test: Get Place by ID
test_case "Get Place by ID"
curl -s -X GET "$API_URL/api/v1/places/$PLACE_ID"
echo ""
echo ""

# ====== REVIEW TESTS ======
section "Review Endpoints"

# Test: Create Valid Review
test_case "Create Valid Review"
REVIEW_RESPONSE=$(curl -s -X POST "$API_URL/api/v1/reviews/" \
     -H "Content-Type: application/json" \
     -d '{
         "text": "Great place to stay!",
         "rating": 5,
         "user_id": "'$USER_ID'",
         "place_id": "'$PLACE_ID'"
     }')
echo "$REVIEW_RESPONSE"

# Extract the review ID for later use
REVIEW_ID=$(echo $REVIEW_RESPONSE | grep -o '"id":"[^"]*' | cut -d'"' -f4)
echo -e "Extracted REVIEW_ID: ${GREEN}$REVIEW_ID${NC}"
echo ""

# Test: Create Review with Empty Text
test_case "Create Review with Empty Text"
curl -s -X POST "$API_URL/api/v1/reviews/" \
     -H "Content-Type: application/json" \
     -d '{
         "text": "",
         "rating": 4,
         "user_id": "'$USER_ID'",
         "place_id": "'$PLACE_ID'"
     }'
echo ""
echo ""

# Test: Create Review with Invalid Rating
test_case "Create Review with Invalid Rating"
curl -s -X POST "$API_URL/api/v1/reviews/" \
     -H "Content-Type: application/json" \
     -d '{
         "text": "Nice place",
         "rating": 6,
         "user_id": "'$USER_ID'",
         "place_id": "'$PLACE_ID'"
     }'
echo ""
echo ""

# Test: Get Review by ID
test_case "Get Review by ID"
curl -s -X GET "$API_URL/api/v1/reviews/$REVIEW_ID"
echo ""
echo ""

# Test: Get Reviews by Place
test_case "Get Reviews by Place"
# Adjust this path according to your API route structure
curl -s -X GET "$API_URL/api/v1/reviews/places/$PLACE_ID"
echo ""
echo ""

# ====== AMENITY TESTS ======
section "Amenity Endpoints"

# Test: Create Valid Amenity
test_case "Create Valid Amenity"
AMENITY_RESPONSE=$(curl -s -X POST "$API_URL/api/v1/amenities/" \
     -H "Content-Type: application/json" \
     -d '{
         "name": "WiFi"
     }')
echo "$AMENITY_RESPONSE"

# Extract the amenity ID for later use
AMENITY_ID=$(echo $AMENITY_RESPONSE | grep -o '"id":"[^"]*' | cut -d'"' -f4)
echo -e "Extracted AMENITY_ID: ${GREEN}$AMENITY_ID${NC}"
echo ""

# Test: Create Amenity with Empty Name
test_case "Create Amenity with Empty Name"
curl -s -X POST "$API_URL/api/v1/amenities/" \
     -H "Content-Type: application/json" \
     -d '{
         "name": ""
     }'
echo ""
echo ""

# Test: Get Amenity by ID
test_case "Get Amenity by ID"
curl -s -X GET "$API_URL/api/v1/amenities/$AMENITY_ID"
echo ""
echo ""

echo -e "${GREEN}==== Testing Completed ====${NC}"
