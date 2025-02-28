import uuid


class HBnBFacade:
    def __init__(self):
        self.amenities = []

    def create_amenity(self, amenity_data):
        """ Creates a new amenity and returns the created object """
        new_amenity = {
            'id': str(uuid.uuid4()),  # Generates a unique ID
            'name': amenity_data['name']
        }
        self.amenities.append(new_amenity)
        return new_amenity

    def get_amenity(self, amenity_id):
        """ Retrieves an amenity by its ID """
        for amenity in self.amenities:
            if amenity['id'] == amenity_id:
                return amenity
        return None  # Returns None if the amenity is not found

    def get_all_amenities(self):
        """ Returns the complete list of amenities """
        return self.amenities

    def update_amenity(self, amenity_id, amenity_data):
        """ Updates an amenity with the provided data """
        for amenity in self.amenities:
            if amenity['id'] == amenity_id:
                amenity['name'] = amenity_data['name']
                return amenity
        return None  # Returns None if the amenity is not found
