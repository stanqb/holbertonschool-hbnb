from .base_model import BaseModel
from .user import User
from .place import Place


class Review(BaseModel):
    def __init__(self, text, rating, place, user):
        super().__init__()
        self.text = self.validate_text(text)
        self.rating = self.validate_rating(rating)
        self.place = self.validate_place(place)
        self.user = self.validate_user(user)

    @staticmethod
    def validate_text(text):
        if not isinstance(text, str) or text.strip() == "":
            raise ValueError("The text cannot be empty.")
        return text

    @staticmethod
    def validate_rating(rating):
        if not isinstance(rating, int) or not (1 <= rating <= 5):
            raise ValueError("The rating must be an integer between 1 and 5.")
        return rating

    @staticmethod
    def validate_place(place):
        if not isinstance(place, Place):
            raise ValueError(
                "The place attribute must be an instance of Place."
            )
        return place

    @staticmethod
    def validate_user(user):
        if not isinstance(user, User):
            raise ValueError("The user attribute must be an instance of User.")
        return user
