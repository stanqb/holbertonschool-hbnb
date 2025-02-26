import re
from hbnb.models.base_model import BaseModel


class User(BaseModel):
    def __init__(self, first_name, last_name, email, is_admin=False):
        super().__init__()
        self.first_name = self.validate_name(first_name)
        self.last_name = self.validate_name(last_name)
        self.email = self.validate_email(email)
        self.is_admin = bool(is_admin)

    @staticmethod
    def validate_name(name):
        if not isinstance(name, str) or len(name) > 50:
            raise ValueError(
                "The name must be a string with a maximum of 50 characters."
            )
        return name

    @staticmethod
    def validate_email(email):
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not isinstance(email, str) or not re.match(pattern, email):
            raise ValueError("Invalid email format.")
        return email
