from uuid import uuid4
from .base_model import BaseModel


class Place(BaseModel):
    def __init__(self, title, description, price, latitude,
                 longitude, owner_id):
        super().__init__()
        self.id = str(uuid4())  # Explicitly defined to match requirements
        self.title = self.validate_title(title)
        self.description = description or ""
        self._price = self.validate_price(price)
        self._latitude = self.validate_latitude(latitude)
        self._longitude = self.validate_longitude(longitude)
        self.owner_id = owner_id  # Store the ID instead of User object
        self.amenities = []  # Keep the amenities list
        self.owner = None  # To store the owner object when needed

    @staticmethod
    def validate_title(title):
        if not isinstance(title, str) or len(title) > 100:
            raise ValueError(
                "The title must be a string with a maximum of 100 characters."
            )
        return title

    @staticmethod
    def validate_price(price):
        if not isinstance(price, (int, float)) or price < 0:
            raise ValueError("The price must be a positive number.")
        return price

    @staticmethod
    def validate_latitude(lat):
        if not isinstance(lat, (int, float)) or not (-90.0 <= lat <= 90.0):
            raise ValueError("Invalid latitude, must be between -90 and 90.")
        return lat

    @staticmethod
    def validate_longitude(lon):
        if not isinstance(lon, (int, float)) or not (-180.0 <= lon <= 180.0):
            raise ValueError(
                "Invalid longitude, must be between -180 and 180."
            )
        return lon

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        self._price = self.validate_price(value)

    @property
    def latitude(self):
        return self._latitude

    @latitude.setter
    def latitude(self, value):
        self._latitude = self.validate_latitude(value)

    @property
    def longitude(self):
        return self._longitude

    @longitude.setter
    def longitude(self, value):
        self._longitude = self.validate_longitude(value)

    def add_amenity(self, amenity):
        """Add an amenity to this place"""
        if amenity not in self.amenities:
            self.amenities.append(amenity)

    def to_dict(self):
        """Convert the object to a dictionary according to API format"""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "owner_id": self.owner_id
        }

    def to_summary_dict(self):
        """Convert the object to a summary dictionary for place listings"""
        return {
            "id": self.id,
            "title": self.title,
            "latitude": self.latitude,
            "longitude": self.longitude
        }

    def to_detail_dict(self):
        """Convert the object to a detailed dictionary with relationships"""
        result = self.to_dict()

        # Add owner information if available
        if self.owner:
            result["owner"] = {
                "id": self.owner.id,
                "first_name": self.owner.first_name,
                "last_name": self.owner.last_name,
                "email": self.owner.email
            }

        # Add amenities information
        result["amenities"] = [
            {"id": amenity.id, "name": amenity.name}
            for amenity in self.amenities
        ]

        return result
