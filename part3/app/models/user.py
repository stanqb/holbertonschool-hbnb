from app import db, bcrypt
import re
from sqlalchemy.orm import validates
from .base_model import BaseModel


class User(BaseModel):
    """User's class"""
    __tablename__ = 'users'

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def __init__(self, first_name, last_name, email, password=None,
                 is_admin=False):
        """user's instance init"""
        super().__init__()  # Call the parent class's __init__ method
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        if password:
            self.hash_password(password)

    @validates('first_name', 'last_name')
    def validate_name(self, key, name):
        """verification of name"""
        if not name or name.strip() == "":
            raise ValueError(f"{key} cannot be empty.")
        return name

    @validates('email')
    def validate_email(self, key, email):
        """verification of email"""
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not email or not re.match(email_pattern, email):
            raise ValueError("Invalid email format.")
        return email

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

    def hash_password(self, password):
        """Hashes the password before storing it."""
        # Use the global instance of Bcrypt
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verifies if the provided password matches the hashed password."""
        # Use the global instance of Bcrypt
        return bcrypt.check_password_hash(self.password, password)

    def to_dict(self):
        """Return a dictionary representation of the user without password"""
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'is_admin': self.is_admin,
            'created_at': self.created_at.isoformat()
            if self.created_at else None,
            'updated_at': self.updated_at.isoformat()
            if self.updated_at else None
        }
