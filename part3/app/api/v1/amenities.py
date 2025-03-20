from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade
from flask_jwt_extended import jwt_required, get_jwt_identity

api = Namespace('amenities', description='Amenity operations')

# Define the amenity model for input validation and documentation
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})

facade = HBnBFacade()


@api.route('/')
class AmenityList(Resource):
    @api.expect(amenity_model)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(401, 'Authentication required')
    @jwt_required()
    def post(self):
        """Register a new amenity (requires authentication)"""
        # Get current user from JWT token
        current_user = get_jwt_identity()

        # Check if user is admin
        # (only admins should be able to create amenities)
        if not current_user.get('is_admin', False):
            return {
                'error': 'Admin privileges required to create amenities'
            }, 403

        amenity_data = api.payload

        # Add validation for empty name
        if not amenity_data.get('name') or amenity_data['name'].strip() == "":
            return {
                'error': 'Invalid input data',
                'details': ['Amenity name cannot be empty']
            }, 400

        new_amenity = facade.create_amenity(amenity_data)
        return {'id': new_amenity.id, 'name': new_amenity.name}, 201

    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """Retrieve a list of all amenities"""
        amenities = facade.get_all_amenities()
        return [
            {'id': amenity.id, 'name': amenity.name}
            for amenity in amenities
        ], 200


@api.route('/<amenity_id>')
class AmenityResource(Resource):
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get amenity details by ID"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404
        return {'id': amenity.id, 'name': amenity.name}, 200

    @api.expect(amenity_model)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    @api.response(401, 'Authentication required')
    @api.response(403, 'Permission denied')
    @jwt_required()
    def put(self, amenity_id):
        """Update an amenity's information (requires authentication)"""
        # Get current user from JWT token
        current_user = get_jwt_identity()

        # Check if user is admin
        # (only admins should be able to update amenities)
        if not current_user.get('is_admin', False):
            return {
                'error': 'Admin privileges required to update amenities'
            }, 403

        amenity_data = api.payload

        # Add validation for empty name
        if not amenity_data.get('name') or amenity_data['name'].strip() == "":
            return {
                'error': 'Invalid input data',
                'details': ['Amenity name cannot be empty']
            }, 400

        updated_amenity = facade.update_amenity(amenity_id, amenity_data)

        if not updated_amenity:
            return {'error': 'Amenity not found'}, 404

        return {'message': 'Amenity updated successfully'}, 200
