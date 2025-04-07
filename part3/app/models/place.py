from app import db
from sqlalchemy.orm import validates, relationship
from .base_model import BaseModel


place_amenity = db.Table(
    'place_amenity',
    db.Column(
        'place_id', db.String(36), db.ForeignKey('places.id'), primary_key=True
    ),
    db.Column(
        'amenity_id', db.String(36),
        db.ForeignKey('amenities.id'),
        primary_key=True
    )
)


class Place(BaseModel):
    """Place model representing a rental property"""
    __tablename__ = 'places'

    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)

    # Foreign key for the owner (User)
    owner_id = db.Column(
        db.String(36), db.ForeignKey('users.id'), nullable=False
    )

    # Relationships
    # One-to-many: Place has many Reviews
    reviews = relationship(
        'Review',
        backref='place',
        lazy='dynamic',
        cascade="all, delete-orphan"
    )

    # Many-to-many: Place has many Amenities
    amenities = relationship(
        'Amenity',
        secondary=place_amenity,
        lazy='subquery',
        backref=db.backref('places', lazy=True)
    )

    # Relationship to the owner (User)
    owner = relationship('User', back_populates='places')

    def __init__(
        self, title, description, price, latitude, longitude, owner_id
    ):
        """Initialize a new place"""
        super().__init__()
        self.title = title
        self.description = description or ""
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner_id = owner_id

    @validates('title')
    def validate_title(self, key, title):
        """Validate the title of the place"""
        if not title or title.strip() == "":
            raise ValueError("Title cannot be empty")
        if len(title) > 100:
            raise ValueError("Title must be a maximum of 100 characters")
        return title

    @validates('price')
    def validate_price(self, key, price):
        """Validate the price of the place"""
        if not isinstance(price, (int, float)) or price <= 0:
            raise ValueError("Price must be a positive number")
        return price

    @validates('latitude')
    def validate_latitude(self, key, latitude):
        """Validate the latitude of the place"""
        if not isinstance(latitude, (int, float)) or not (
            -90.0 <= latitude <= 90.0
        ):
            raise ValueError("Latitude must be between -90 and 90")
        return latitude

    @validates('longitude')
    def validate_longitude(self, key, longitude):
        """Validate the longitude of the place"""
        if not isinstance(longitude, (int, float)) or not (
            -180.0 <= longitude <= 180.0
        ):
            raise ValueError("Longitude must be between -180 and 180")
        return longitude

    def add_amenity(self, amenity):
        """Add an amenity to this place"""
        if amenity not in self.amenities:
            self.amenities.append(amenity)

    def to_dict(self):
        """Return a dictionary representation of the place"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'owner_id': self.owner_id,
            'created_at': (
                self.created_at.isoformat() if self.created_at else None
            ),
            'updated_at': (
                self.updated_at.isoformat() if self.updated_at else None
            )
        }

    def to_summary_dict(self):
        """Return a summarized dictionary representation of the place"""
        return {
            'id': self.id,
            'title': self.title,
            'latitude': self.latitude,
            'longitude': self.longitude
        }

    def to_detail_dict(self):
        """Return a detailed dictionary representation of the place
        with relationships"""
        result = self.to_dict()

        # Add owner information if available
        if self.owner:
            result['owner'] = {
                'id': self.owner.id,
                'first_name': self.owner.first_name,
                'last_name': self.owner.last_name,
                'email': self.owner.email
            }

        # Add amenities information
        result['amenities'] = [
            {'id': amenity.id, 'name': amenity.name}
            for amenity in self.amenities
        ]

        return result
