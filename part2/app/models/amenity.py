import uuid


class Amenity:
    def __init__(self, name):
        self.name = self.validate_name(name)
        self.id = str(uuid.uuid4())

    @staticmethod
    def validate_name(name):
        if not isinstance(name, str) or len(name) > 50:
            raise ValueError(
                "The name of the amenity must be a string with a maximum of "
                "50 characters."
            )
        return name

    def update(self, updated_data):
        """Update the informations"""
        self.name = updated_data.get('name', self.name)