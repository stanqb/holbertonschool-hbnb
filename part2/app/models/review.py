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

    def validate(self, facade=None):
        """Validate all review data and return a list of errors"""
        errors = []

        # Validate text
        if not isinstance(self.text, str) or self.text.strip() == "":
            errors.append("Review text cannot be empty")

        # Validate rating
        try:
            rating = int(self.rating)
            if not (1 <= rating <= 5):
                errors.append("Rating must be an integer between 1 and 5")
        except (ValueError, TypeError):
            errors.append("Rating must be an integer between 1 and 5")

        # Validate user_id and place_id
        if not self.user_id:
            errors.append("User ID cannot be empty")

        if not self.place_id:
            errors.append("Place ID cannot be empty")

        # If a facade is provided, validate that IDs reference valid entities
        if facade:
            try:
                if not facade.get_user_by_id(self.user_id):
                    errors.append("Invalid user_id - user not found")
            except Exception:
                errors.append("Invalid user_id - user not found")

            try:
                if not facade.get_place_by_id(self.place_id):
                    errors.append("Invalid place_id - place not found")
            except Exception:
                errors.append("Invalid place_id - place not found")

        return errors

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
