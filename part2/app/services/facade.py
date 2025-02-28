from app.models.amenity import Amenity
from app.persistence.repository import Repository


class HBnBFacade:
    def __init__(self):
        self.repository = Repository()

    def create_amenity(self, amenity_data):
        """Creates a new amenity and saves it to the database."""
        if 'name' not in amenity_data or not amenity_data['name']:
            return None, "Amenity name required"
        new_amenity = Amenity(name=amenity_data['name'])
        self.repository.save(new_amenity)
        return new_amenity, None

    def get_amenity(self, amenity_id):
        """Retrieves an amenity by its ID."""
        return self.repository.get_by_id(Amenity, amenity_id)

    def get_all_amenities(self):
        """Retrieves all available amenities."""
        return self.repository.get_all(Amenity)

    def update_amenity(self, amenity_id, amenity_data):
        """Updates the information of an existing amenity."""
        amenity = self.repository.get_by_id(Amenity, amenity_id)
        if not amenity:
            return None, "Amenity not found"
        if 'name' in amenity_data and amenity_data['name']:
            amenity.name = amenity_data['name']
            self.repository.save(amenity)
            return amenity, None
        return None, "Invalid data"
