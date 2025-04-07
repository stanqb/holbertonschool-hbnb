import os
from app import create_app
from app.services.facade import HBnBFacade

# Get the configuration from environment variable or use default
flask_env = os.getenv('FLASK_ENV', 'development')

# Create a mapping between environment names and config classes
config_mapping = {
    'development': 'config.DevelopmentConfig',
    'testing': 'config.TestingConfig',
    'production': 'config.ProductionConfig'
}

# Get the appropriate config class or default to DevelopmentConfig
config_class = config_mapping.get(flask_env, 'config.DevelopmentConfig')

# Create app with the selected config
app = create_app(config_class)

# Add a test user for development
if __name__ == '__main__':
    # Create a test user if the application is in development mode
    if app.config['DEBUG']:
        facade = HBnBFacade()
        try:
            # Check if the user already exists
            test_user = facade.get_user_by_email('test@example.com')
            if not test_user:
                # Create the test user
                user_data = {
                    'first_name': 'Test',
                    'last_name': 'User',
                    'email': 'test@example.com',
                    'password': 'testpassword'
                }
                test_user = facade.create_user(user_data)
                print(f"Test user created successfully: {test_user.to_dict()}")
            else:
                print(f"Test user already exists: {test_user.to_dict()}")
        except Exception as e:
            print(f"Error creating test user: {e}")

    app.run(debug=True)
