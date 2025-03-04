from .base_model import BaseModel


class Review(BaseModel):
    def __init__(self, text, rating, place_id, user_id):
        super().__init__()
        self.text = self.validate_text(text)
        self.rating = self.validate_rating(rating)
        self.place_id = place_id
        self.user_id = user_id

    @staticmethod
    def validate_text(text):
        if not isinstance(text, str) or text.strip() == "":
            raise ValueError("The text cannot be empty.")
        return text

    @staticmethod
    def validate_rating(rating):
        try:
            rating = int(rating)
            if not (1 <= rating <= 5):
                raise ValueError()
        except (ValueError, TypeError):
            raise ValueError("The rating must be an integer between 1 and 5.")
        return rating

    def to_dict(self):
        """Return a dictionary representation of the review"""
        return {
            'id': self.id,
            'text': self.text,
            'rating': self.rating,
            'user_id': self.user_id,
            'place_id': self.place_id,
            'created_at': (self.created_at.isoformat()
                           if hasattr(self.created_at, 'isoformat')
                           else self.created_at),
            'updated_at': (self.updated_at.isoformat()
                           if hasattr(self.updated_at, 'isoformat')
                           else self.updated_at)
        }
