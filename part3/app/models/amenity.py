from app import db
from sqlalchemy.orm import validates
from .base_model import BaseModel


class Amenity(BaseModel):
    """Amenity model representing a feature available at places"""
    __tablename__ = 'amenities'

    name = db.Column(db.String(50), nullable=False)

    def __init__(self, name):
        """Initialize a new amenity"""
        super().__init__()  # Call the parent class's __init__ method
        self.name = name

    @validates('name')
    def validate_name(self, key, name):
        """Validate the name of the amenity"""
        if not name or name.strip() == "":
            raise ValueError("Amenity name cannot be empty")
        if len(name) > 50:
            raise ValueError("Amenity name must be a maximum of 50 characters")
        return name

    def update(self, updated_data):
        """Update the amenity information"""
        if 'name' in updated_data:
            self.name = self.validate_name('name', updated_data['name'])

    def to_dict(self):
        """Return a dictionary representation of the amenity"""
        return {
            'id': self.id,
            'name': self.name,
            'created_at': (
                self.created_at.isoformat() if self.created_at else None
            ),
            'updated_at': (
                self.updated_at.isoformat() if self.updated_at else None
            )
        }
