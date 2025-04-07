from app import db, bcrypt
import re
from sqlalchemy.orm import validates, relationship
from .base_model import BaseModel


class User(BaseModel):
    """User model representing an application user"""
    __tablename__ = 'users'

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    # Relationships
    # One-to-many: User has many Places
    places = relationship(
        'Place',
        back_populates='owner',
        lazy='dynamic',
        cascade="all, delete-orphan"
    )

    # One-to-many: User has many Reviews
    reviews = relationship(
        'Review',
        backref='user',
        lazy='dynamic',
        cascade="all, delete-orphan"
    )

    def __init__(
        self, first_name, last_name, email, password=None, is_admin=False
    ):
        """Initialize a new user"""
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        if password:
            self.hash_password(password)

    @validates('first_name', 'last_name')
    def validate_name(self, key, name):
        """Validate the first name and last name of the user"""
        if not name or name.strip() == "":
            raise ValueError(f"{key} cannot be empty.")
        return name

    @validates('email')
    def validate_email(self, key, email):
        """Validate the email of the user"""
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not email or not re.match(email_pattern, email):
            raise ValueError("Invalid email format.")
        return email

    def hash_password(self, password):
        """Hash the password before storing it"""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verify that the provided password matches the stored hash"""
        return bcrypt.check_password_hash(self.password, password)

    def to_dict(self):
        """
        Return a dictionary representation of the user without the password
        """
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'is_admin': self.is_admin,
            'created_at': (
                self.created_at.isoformat() if self.created_at else None
            ),
            'updated_at': (
                self.updated_at.isoformat() if self.updated_at else None
            )
        }
