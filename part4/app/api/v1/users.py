from flask_restx import Namespace, Resource, fields
from app.services import facade
import re
from flask_jwt_extended import jwt_required, get_jwt_identity

api = Namespace('users', description='User operations')

# Define the user model for input validation and documentation
user_model = api.model('User', {
    'first_name': fields.String(
        required=True,
        description='First name of the user'
    ),
    'last_name': fields.String(
        required=True,
        description='Last name of the user'
    ),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(
        required=True,
        description='Password for authentication'
    ),
    'is_admin': fields.Boolean(description='Admin status flag')
})

# Model for updating user information
user_update_model = api.model('UserUpdate', {
    'first_name': fields.String(description='First name of the user'),
    'last_name': fields.String(description='Last name of the user'),
    'email': fields.String(description='Email of the user'),
    'password': fields.String(description='Password for authentication'),
    'is_admin': fields.Boolean(description='Admin status flag')
})


@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    @api.response(401, 'Authentication required')
    @api.response(403, 'Admin privileges required')
    @jwt_required()
    def post(self):
        """Create a new user (admin access only)"""
        # Check if user is admin
        current_user = get_jwt_identity()
        if not current_user.get('is_admin', False):
            return {'error': 'Admin privileges required'}, 403

        user_data = api.payload

        # Check for existing email
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400

        # Manual validation of the data
        errors = []

        # Validate first_name
        if not user_data.get('first_name') or \
           user_data['first_name'].strip() == "":
            errors.append("First name cannot be empty")

        # Validate last_name
        if not user_data.get('last_name') or \
           user_data['last_name'].strip() == "":
            errors.append("Last name cannot be empty")

        # Validate email format
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not user_data.get('email') or not re.match(
                email_pattern, user_data['email']):
            errors.append("Invalid email format")

        # Validate password
        if not user_data.get('password') or len(user_data['password']) < 6:
            errors.append(
                "Password is required and must be at least 6 characters long"
            )

        # Return errors if any
        if errors:
            return {'error': 'Invalid input data', 'details': errors}, 400

        new_user = facade.create_user(user_data)
        return {
            'id': new_user.id,
            'first_name': new_user.first_name,
            'last_name': new_user.last_name,
            'email': new_user.email,
            'is_admin': new_user.is_admin
        }, 201

    @api.response(200, 'User list successfully retrieved')
    @api.response(401, 'Authentication required')
    @jwt_required()
    def get(self):
        """Get list of all users (requires authentication)"""
        # Check if the user is an admin
        current_user = get_jwt_identity()
        if not current_user.get('is_admin', False):
            return {'error': 'Admin privileges required'}, 403

        users = facade.user_repo.get_all()
        return [
            {
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'is_admin': user.is_admin
            }
            for user in users
        ], 200


@api.route('/<user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    @api.response(401, 'Authentication required')
    @api.response(403, 'Access denied')
    @jwt_required()
    def get(self, user_id):
        """Get user details by ID (requires authentication)"""
        # Get current user from JWT token
        current_user = get_jwt_identity()

        # Check if the user is requesting their own data or is an admin
        if (str(user_id) != current_user and
                not current_user.get('is_admin', False)):
            return {'error': 'Access denied'}, 403

        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'is_admin': user.is_admin
        }, 200

    @api.expect(user_update_model)
    @api.response(200, 'User updated successfully')
    @api.response(400, 'Invalid input data')
    @api.response(401, 'Authentication required')
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'User not found')
    @jwt_required()
    def put(self, user_id):
        """Modify user information (requires authentication)"""
        # Get current user from JWT token
        current_user = get_jwt_identity()

        # Get the user data from request
        user_data = api.payload

        # Check if user is the same as the one being modified or an admin
        is_admin = current_user.get('is_admin', False)
        is_same_user = str(user_id) == current_user

        # If not the same user and not an admin
        if not is_same_user and not is_admin:
            return {'error': 'Unauthorized action'}, 403

        # Regular users can't modify email or password
        if not is_admin and ('email' in user_data or 'password' in user_data):
            return {'error': 'You cannot modify email or password'}, 400

        # For admins, check email uniqueness
        if is_admin and 'email' in user_data:
            existing_user = facade.get_user_by_email(user_data['email'])
            if existing_user and existing_user.id != user_id:
                return {'error': 'Email is already in use'}, 400

        # Validate first_name if provided
        if 'first_name' in user_data and (
            not user_data.get('first_name') or
            user_data['first_name'].strip() == ""
        ):
            return {'error': 'First name cannot be empty'}, 400

        # Validate last_name if provided
        if 'last_name' in user_data and (not user_data.get('last_name') or
                                         user_data['last_name'].strip() == ""):
            return {'error': 'Last name cannot be empty'}, 400

        # Validate email format if provided
        if 'email' in user_data:
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not user_data['email'] or not re.match(
                    email_pattern, user_data['email']):
                return {'error': 'Invalid email format'}, 400

        # Validate password if provided
        if 'password' in user_data and len(user_data['password']) < 6:
            return {
                'error': 'Password must be at least 6 characters long'
            }, 400

        # Update user
        updated_user = facade.update_user(user_id, user_data)
        if not updated_user:
            return {'error': 'User not found'}, 404

        return {
            'id': updated_user.id,
            'first_name': updated_user.first_name,
            'last_name': updated_user.last_name,
            'email': updated_user.email,
            'is_admin': updated_user.is_admin
        }, 200
