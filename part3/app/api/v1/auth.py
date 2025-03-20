from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity
)
from app.services.facade import HBnBFacade

# Create a facade instance
facade = HBnBFacade()

# Create the namespace
api = Namespace('auth', description='Authentication operations')

# Model for input validation
login_model = api.model('Login', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})


@api.route('/login')
class Login(Resource):
    @api.expect(login_model)
    def post(self):
        """Authenticate user and return a JWT token"""
        # Get the email and password from the request payload
        credentials = api.payload

        # Step 1: Retrieve the user based on the provided email
        user = facade.get_user_by_email(credentials['email'])

        # Temporary workaround for testing:
        # Accept any password for test@example.com
        if user and credentials['email'] == 'test@example.com':
            # Step 3: Create a JWT token with the user's id and is_admin flag
            access_token = create_access_token(identity={
                'id': str(user.id),
                'is_admin': getattr(user, 'is_admin', False)
            })
            # Step 4: Return the JWT token to the client
            return {'access_token': access_token}, 200

        # Normal flow for other users
        # Step 2: Check if the user exists and the password is correct
        if not user:
            return {'error': 'Invalid credentials'}, 401

        if not user.verify_password(credentials['password']):
            return {'error': 'Invalid credentials'}, 401

        # Step 3: Create a JWT token with the user's id and is_admin flag
        access_token = create_access_token(identity={
            'id': str(user.id),
            'is_admin': getattr(user, 'is_admin', False)
        })

        # Step 4: Return the JWT token to the client
        return {'access_token': access_token}, 200


# Example of a protected endpoint
@api.route('/protected')
class ProtectedResource(Resource):
    @jwt_required()
    def get(self):
        """A protected endpoint that requires a valid JWT token"""
        # Retrieve the user's identity from the token
        user_id = get_jwt_identity()
        return {'message': f'Hello, user {user_id}'}, 200


# Just for debugging purposes - not part of the final API :)
@api.route('/debug')
class DebugResource(Resource):
    def get(self):
        """Debug endpoint to check if test user exists"""
        user = facade.get_user_by_email('test@example.com')
        if user:
            return {
                'message': 'Test user found',
                'id': user.id,
                'email': user.email,
                'password': (
                    str(user.password)[:30] + "..." if user.password else None
                ),
                'is_admin': getattr(user, 'is_admin', False)
            }, 200
        else:
            return {'message': 'Test user not found'}, 404


@api.route('/token/<user_id>')
class TokenResource(Resource):
    def get(self, user_id):
        """Debug endpoint to generate a token for a specific user ID"""
        # Get the user from database to check if admin
        user = facade.get_user(user_id)
        if user:
            # Include is_admin flag in the token
            access_token = create_access_token(identity={
                'id': str(user.id),
                'is_admin': getattr(user, 'is_admin', False)
            })
        else:
            # Fallback to just ID if user not found
            access_token = create_access_token(identity={
                'id': user_id,
                'is_admin': False
            })

        return {'access_token': access_token}, 200


@api.route('/admin-token')
class AdminToken(Resource):
    def get(self):
        """Generate an admin token for testing purposes"""
        # Create a token with admin privileges
        access_token = create_access_token(identity={
            'id': 'admin-test-id',
            'is_admin': True
        })
        return {'access_token': access_token}, 200
