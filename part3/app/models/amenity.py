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

    def validate(self):
        """Validate all amenity data and return a list of errors"""
        errors = []

        # Validate name
        if not self.name or self.name.strip() == "":
            errors.append("Amenity name cannot be empty")
        elif len(self.name) > 50:
            errors.append("Amenity name must be a maximum of 50 characters")

        return errors

    def update(self, updated_data):
        """Update the informations"""
        self.name = updated_data.get('name', self.name)

    def to_dict(self):
        """Return a dictionary representation of the amenity"""
        return {
            'id': self.id,
            'name': self.name
        }
