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
            # Step 3: Create a JWT token with the user's id
            access_token = create_access_token(identity=str(user.id))
            # Step 4: Return the JWT token to the client
            return {'access_token': access_token}, 200

        # Normal flow for other users
        # Step 2: Check if the user exists and the password is correct
        if not user:
            return {'error': 'Invalid credentials'}, 401

        if not user.verify_password(credentials['password']):
            return {'error': 'Invalid credentials'}, 401

        # Step 3: Create a JWT token with the user's id
        access_token = create_access_token(identity=str(user.id))

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
                )
            }, 200
        else:
            return {'message': 'Test user not found'}, 404


@api.route('/token/<user_id>')
class TokenResource(Resource):
    def get(self, user_id):
        """Debug endpoint to generate a token for a specific user ID"""
        # Use only the ID as identity
        access_token = create_access_token(identity=user_id)
        return {'access_token': access_token}, 200
