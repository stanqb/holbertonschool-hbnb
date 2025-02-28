from app.models.amenity import Amenity
from app.persistence.repository import Repository
from flask import request
from flask_restx import Namespace, Resource

api = Namespace('amenities', description='Operations related to amenities')


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


facade = HBnBFacade()


@api.route('/')
class AmenityListResource(Resource):
    def get(self):
        """Returns the list of all amenities."""
        return [amenity.to_dict() for amenity in facade.get_all_amenities()]

    def post(self):
        """Creates a new amenity."""
        amenity_data = request.json
        amenity, error = facade.create_amenity(amenity_data)
        if error:
            return {'error': error}, 400
        return amenity.to_dict(), 201


@api.route('/<int:amenity_id>')
class AmenityResource(Resource):
    def get(self, amenity_id):
        """Returns an amenity by its ID."""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': "Amenity not found"}, 404
        return amenity.to_dict()

    def put(self, amenity_id):
        """Updates an amenity."""
        amenity_data = request.json
        amenity, error = facade.update_amenity(amenity_id, amenity_data)
        if error:
            return {'error': error}, 400
        return amenity.to_dict()

    def delete(self, amenity_id):
        """Deletes an amenity."""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': "Amenity not found"}, 404
        facade.repository.delete(amenity)
        return {}, 204
