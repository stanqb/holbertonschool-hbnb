from .base_model import BaseModel
from .user import User


class Place(BaseModel):
    def __init__(self, title, description, price, latitude, longitude, owner):
        super().__init__()
        self.title = self.validate_title(title)
        self.description = description or ""
        self.price = self.validate_price(price)
        self.latitude = self.validate_latitude(latitude)
        self.longitude = self.validate_longitude(longitude)
        self.owner = self.validate_owner(owner)
        self.reviews = []
        self.amenities = []

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

    @staticmethod
    def validate_owner(owner):
        if not isinstance(owner, User):
            raise ValueError(
                "The owner attribute must be an instance of User."
            )
        return owner

    def add_review(self, review):
        self.reviews.append(review)

    def add_amenity(self, amenity):
        self.amenities.append(amenity)
