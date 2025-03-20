from app import create_app
from app.services.facade import HBnBFacade

app = create_app()

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
