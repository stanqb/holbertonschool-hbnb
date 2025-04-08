from flask import Flask
from flask_restx import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy

# Initialize Bcrypt
bcrypt = Bcrypt()

# Initialize JWTManager
jwt = JWTManager()

# Initialize SQLAlchemy
db = SQLAlchemy()


def create_app(config_class="config.DevelopmentConfig"):
    """
    Application factory function that creates and configures the Flask app.
    Args:
        config_class (str): The configuration class to use for the app.
                           Defaults to "config.DevelopmentConfig".
    Returns:
        Flask: The configured Flask application instance.
    """
    app = Flask(__name__)

    # Configure the app from the config_class
    app.config.from_object(config_class)

    # Set JWT to use the same secret key as the app
    app.config['JWT_SECRET_KEY'] = app.config['SECRET_KEY']

    # Initialize Bcrypt with the application
    bcrypt.init_app(app)

    # Initialize JWTManager with the application
    jwt.init_app(app)

    # Initialize SQLAlchemy with the application
    db.init_app(app)

    api = Api(
        app,
        version='1.0',
        title='HBnB API',
        description='HBnB Application API'
    )

    # Import namespaces here to avoid circular imports
    from app.api.v1.users import api as users_ns
    from app.api.v1.amenities import api as amenities_ns
    from app.api.v1.reviews import api as reviews_ns
    from app.api.v1.places import api as places_ns
    from app.api.v1.auth import api as auth_ns

    # Register the namespaces
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(auth_ns, path='/api/v1/auth')

    return app
