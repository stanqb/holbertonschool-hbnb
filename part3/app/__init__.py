from flask import Flask
from flask_restx import Api
from flask_bcrypt import Bcrypt
from app.api.v1.users import api as users_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.reviews import api as reviews_ns
from app.api.v1.places import api as places_ns

# Initialiser Bcrypt
bcrypt = Bcrypt()


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
    app.config.from_object(config_class)

    # Initialiser Bcrypt avec l'application
    bcrypt.init_app(app)

    api = Api(
        app,
        version='1.0',
        title='HBnB API',
        description='HBnB Application API'
    )

    # Register the namespaces
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    api.add_namespace(places_ns, path='/api/v1/places')

    return app
