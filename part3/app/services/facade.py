from app.models.amenity import Amenity


def create_amenity(self, amenity_data):
    """Creates a new amenity with validation.

    Args:
        amenity_data (dict): Amenity data containing name

    Returns:
        Amenity: Created amenity object
    """
    # Extract amenity name from data
    name = amenity_data.get('name')

    # Create and save the amenity
    # (using the already imported model from the top of the file)
    amenity = Amenity(name=name)
    self.amenity_repo.add(amenity)
    return amenity


def update_amenity(self, amenity_id, amenity_data):
    """Updates the information of an existing amenity.

    Args:
        amenity_id (str): ID of the amenity to update
        amenity_data (dict): Updated amenity data

    Returns:
        Amenity: Updated amenity object or None if not found
    """
    # Get the amenity
    amenity = self.amenity_repo.get(amenity_id)
    if not amenity:
        return None

    # Update the amenity with new data
    if 'name' in amenity_data:
        self.amenity_repo.update(amenity_id, {'name': amenity_data['name']})

    # Return the updated amenity
    return self.amenity_repo.get(amenity_id)
