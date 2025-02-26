from .base_model import BaseModel


class Amenity(BaseModel):
    def __init__(self, name):
        super().__init__()
        self.name = self.validate_name(name)

    @staticmethod
    def validate_name(name):
        if not isinstance(name, str) or len(name) > 50:
            raise ValueError(
                "The name of the amenity must be a string with a maximum of "
                "50 characters."
            )
        return name
