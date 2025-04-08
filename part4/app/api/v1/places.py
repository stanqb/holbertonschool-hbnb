from flask import request
from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity

api = Namespace('places', description='Place operations')

# Simplified user model for nested display
user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the user'),
    'last_name': fields.String(description='Last name of the user'),
    'email': fields.String(description='Email of the user')
})

# Simplified amenity model for nested display
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

# Adding the review model
review_model = api.model('PlaceReview', {
    'id': fields.String(description='Review ID'),
    'text': fields.String(description='Text of the review'),
    'rating': fields.Integer(description='Rating of the place (1-5)'),
    'user_id': fields.String(description='ID of the user')
})

# Model for inputs
place_input_model = api.model('PlaceInput', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True,
                             description='Latitude of the place'),
    'longitude': fields.Float(required=True,
                              description='Longitude of the place')
})

# Model for updates
place_update_model = api.model('PlaceUpdate', {
    'title': fields.String(description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(description='Price per night'),
    'latitude': fields.Float(description='Latitude of the place'),
    'longitude': fields.Float(description='Longitude of the place')
})

# Detailed place model for responses (including relationships)
place_detail_model = api.model('PlaceDetail', {
    'id': fields.String(description='Place ID'),
    'title': fields.String(description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(description='Price per night'),
    'latitude': fields.Float(description='Latitude of the place'),
    'longitude': fields.Float(description='Longitude of the place'),
    'owner_id': fields.String(description='ID of the owner'),
    'owner': fields.Nested(user_model, description='Owner of the place'),
    'amenities': fields.List(
        fields.Nested(amenity_model),
        description='List of amenities'
    ),
    'reviews': fields.List(
        fields.Nested(review_model),
        description='List of reviews'
    )
})


@api.route('/')
class PlaceList(Resource):
    @api.expect(place_input_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(401, 'Authentication required')
    @jwt_required()
    def post(self):
        """Register a new place (requires authentication)"""
        # Get current user ID from JWT token
        current_user = get_jwt_identity()
        data = request.get_json()

        # Set owner_id to current user's id
        data['owner_id'] = current_user

        # Manual validation of the data
        errors = []

        # Validate title
        if not data.get('title') or data['title'].strip() == "":
            errors.append("Title cannot be empty")
        elif len(data.get('title', '')) > 100:
            errors.append("Title must be a maximum of 100 characters")

        # Validate price
        if not isinstance(data.get('price'), (int, float)):
            errors.append("Price must be a number")
        elif data.get('price', 0) <= 0:
            errors.append("Price must be a positive number")

        # Validate latitude
        if not isinstance(data.get('latitude'), (int, float)):
            errors.append("Latitude must be a number")
        elif not (-90.0 <= data.get('latitude', 0) <= 90.0):
            errors.append("Latitude must be between -90 and 90")

        # Validate longitude
        if not isinstance(data.get('longitude'), (int, float)):
            errors.append("Longitude must be a number")
        elif not (-180.0 <= data.get('longitude', 0) <= 180.0):
            errors.append("Longitude must be between -180 and 180")

        # Return errors if any
        if errors:
            return {'error': 'Invalid input data', 'details': errors}, 400

        try:
            new_place = facade.create_place(data)
            return new_place, 201
        except ValueError as e:
            return {'error': str(e)}, 400

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places"""
        places = facade.get_all_places()
        return places, 200


@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        place = facade.get_place_by_id(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        return place, 200

    @api.expect(place_update_model)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    @api.response(401, 'Authentication required')
    @api.response(403, 'Unauthorized action')
    @jwt_required()
    def put(self, place_id):
        """Update a place's information (requires authentication)"""
        # Get current user ID from JWT token
        current_user = get_jwt_identity()

        # Set is_admin default to False if not exists
        is_admin = current_user.get('is_admin', False)

        data = request.get_json()

        # Get the existing place
        existing_place = facade.get_place_by_id(place_id)
        if not existing_place:
            return {'error': 'Place not found'}, 404

        # Check if user is the owner of the place or an admin
        if not is_admin and existing_place.get('owner_id') != current_user:
            return {'error': 'Unauthorized action'}, 403

        # Manual validation of the data
        errors = []

        # Validate title
        if 'title' in data:
            if not data.get('title') or data['title'].strip() == "":
                errors.append("Title cannot be empty")
            elif len(data.get('title', '')) > 100:
                errors.append("Title must be a maximum of 100 characters")

        # Validate price
        if 'price' in data:
            if not isinstance(data.get('price'), (int, float)):
                errors.append("Price must be a number")
            elif data.get('price', 0) <= 0:
                errors.append("Price must be a positive number")

        # Validate latitude
        if 'latitude' in data:
            if not isinstance(data.get('latitude'), (int, float)):
                errors.append("Latitude must be a number")
            elif not (-90.0 <= data.get('latitude', 0) <= 90.0):
                errors.append("Latitude must be between -90 and 90")

        # Validate longitude
        if 'longitude' in data:
            if not isinstance(data.get('longitude'), (int, float)):
                errors.append("Longitude must be a number")
            elif not (-180.0 <= data.get('longitude', 0) <= 180.0):
                errors.append("Longitude must be between -180 and 180")

        # Return errors if any
        if errors:
            return {'error': 'Invalid input data', 'details': errors}, 400

        try:
            result = facade.update_place(place_id, data)
            if not result:
                return {'error': 'Place not found'}, 404
            return {'message': 'Place updated successfully'}, 200
        except ValueError as e:
            return {'error': str(e)}, 400
