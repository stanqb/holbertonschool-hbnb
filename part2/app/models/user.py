import uuid
import re


class User:
    """User's class"""
    def __init__(self, first_name, last_name, email, password=None):
        """user's instance init"""
        self.id = str(uuid.uuid4())
<<<<<<< HEAD
        self.first_name = self.validate_name(first_name)
        self.last_name = self.validate_name(last_name)
        self.email = self.validate_email(email)
        self.password = self.validate_password(password)
=======
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
>>>>>>> 768504cb6c5581ea375d3c4df2d20e8f3fdbea47

    def validate_name(self, name):
        """verification of name"""
        if not name:
            raise ValueError("First name and last name cannot be empty.")
        return name

    def validate_email(self, email):
        """verification of email"""
        if not email or '@' not in email or '.' not in email.split('@')[-1]:
            raise ValueError("Invalid email format.")
        return email

<<<<<<< HEAD
    def validate_password(self, password):
        """Verification of password length"""
        if not password or len(password) <= 5:
            raise ValueError("Password must be longer than 5 characters.")
        return password
=======
    def validate(self):
        """Validate all user data and return a list of errors"""
        errors = []

        # Validate first_name
        if not self.first_name or self.first_name.strip() == "":
            errors.append("First name cannot be empty")

        # Validate last_name
        if not self.last_name or self.last_name.strip() == "":
            errors.append("Last name cannot be empty")

        # Validate email format with a more detailed regex
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not self.email or not re.match(email_pattern, self.email):
            errors.append("Invalid email format")

        return errors
>>>>>>> 768504cb6c5581ea375d3c4df2d20e8f3fdbea47

    def update(self, updated_data):
        """instance to update user's data"""
        self.first_name = updated_data.get('first_name', self.first_name)
        self.last_name = updated_data.get('last_name', self.last_name)
        self.email = updated_data.get('email', self.email)
        if 'password' in updated_data:
            self.password = self.validate_password(updated_data['password'])

    def to_dict(self):
        """Return a dictionary representation of the user"""
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email
        }
