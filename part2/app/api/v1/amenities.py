from app.models.amenity import Amenity
from app.persistence.repository import Repository
from flask import request
from flask_restx import Namespace, Resource

api = Namespace('amenities', description='Operations liées aux amenities')


class HBnBFacade:
    def __init__(self):
        self.repository = Repository()

    def create_amenity(self, amenity_data):
        """Crée une nouvelle amenity et l'enregistre
        dans la base de données."""
        if 'name' not in amenity_data or not amenity_data['name']:
            return None, "Nom de l'amenity requis"
        new_amenity = Amenity(name=amenity_data['name'])
        self.repository.save(new_amenity)
        return new_amenity, None

    def get_amenity(self, amenity_id):
        """Récupère une amenity par son ID."""
        return self.repository.get_by_id(Amenity, amenity_id)

    def get_all_amenities(self):
        """Récupère toutes les amenities disponibles."""
        return self.repository.get_all(Amenity)

    def update_amenity(self, amenity_id, amenity_data):
        """Met à jour les informations d'une amenity existante."""
        amenity = self.repository.get_by_id(Amenity, amenity_id)
        if not amenity:
            return None, "Amenity introuvable"
        if 'name' in amenity_data and amenity_data['name']:
            amenity.name = amenity_data['name']
            self.repository.save(amenity)
            return amenity, None
        return None, "Données invalides"


facade = HBnBFacade()


@api.route('/')
class AmenityListResource(Resource):
    def get(self):
        """Retourne la liste de toutes les amenities."""
        return [amenity.to_dict() for amenity in facade.get_all_amenities()]

    def post(self):
        """Crée une nouvelle amenity."""
        amenity_data = request.json
        amenity, error = facade.create_amenity(amenity_data)
        if error:
            return {'error': error}, 400
        return amenity.to_dict(), 201


@api.route('/<int:amenity_id>')
class AmenityResource(Resource):
    def get(self, amenity_id):
        """Retourne une amenity par son ID."""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': "Amenity introuvable"}, 404
        return amenity.to_dict()

    def put(self, amenity_id):
        """Met à jour une amenity."""
        amenity_data = request.json
        amenity, error = facade.update_amenity(amenity_id, amenity_data)
        if error:
            return {'error': error}, 400
        return amenity.to_dict()

    def delete(self, amenity_id):
        """Supprime une amenity."""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': "Amenity introuvable"}, 404
        facade.repository.delete(amenity)
        return {}, 204
