from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.persistence.repository import InMemoryRepository


class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()

    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

    def update_user(self, user_id, updated_data):
        """Update user informations"""
        user = self.user_repo.get(user_id)
        if user:
            user.update(updated_data)
            return user
        return None

    def create_amenity(self, amenity_data):
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        """Retrieves an amenity by its ID."""
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        """Retrieves all available amenities."""
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        """Updates the information of an existing amenity."""
        amenity = self.amenity_repo.get(amenity_id)
        if amenity:
            amenity.update(amenity_data)
            return amenity
        return None

    def create_place(self, place_data):
        """Creates a new place with validation of attributes."""
        owner_id = place_data.get("owner_id")
        # Verify owner exists
        if not self.user_repo.get(owner_id):
            raise ValueError("Invalid owner ID.")

        place = Place(
            title=place_data["title"],
            description=place_data.get("description", ""),
            price=place_data["price"],
            latitude=place_data["latitude"],
            longitude=place_data["longitude"],
            owner_id=owner_id
        )

        # Add amenities if provided
        if "amenities" in place_data and place_data["amenities"]:
            for amenity_id in place_data["amenities"]:
                amenity = self.amenity_repo.get(amenity_id)
                if amenity:
                    place.add_amenity(amenity)

        self.place_repo.add(place)
        # Return in the format expected by the API
        return place.to_dict()

    def get_place_by_id(self, place_id):
        """Retrieves a place by ID, including its owner and amenities."""
        place = self.place_repo.get(place_id)
        if not place:
            return None

        # Load owner relationship
        place.owner = self.user_repo.get(place.owner_id)

        # Return in the detailed format expected by the API
        return place.to_detail_dict()

    def get_all_places(self):
        """Retrieves all places in a summarized format."""
        places = self.place_repo.get_all()
        # Return in the summarized format expected by the API
        return [place.to_summary_dict() for place in places]

    def update_place(self, place_id, place_data):
        """Updates a place's details while ensuring data integrity."""
        place = self.place_repo.get(place_id)
        if not place:
            return None

        if "title" in place_data:
            place.title = Place.validate_title(place_data["title"])
        if "description" in place_data:
            place.description = place_data["description"]
        if "price" in place_data:
            place.price = place_data["price"]
        if "latitude" in place_data:
            place.latitude = place_data["latitude"]
        if "longitude" in place_data:
            place.longitude = place_data["longitude"]
        if "owner_id" in place_data:
            owner_id = place_data["owner_id"]
            if self.user_repo.get(owner_id):
                place.owner_id = owner_id

        # Update amenities if provided
        if "amenities" in place_data:
            # Clear existing amenities
            place.amenities = []
            # Add new amenities
            for amenity_id in place_data["amenities"]:
                amenity = self.amenity_repo.get(amenity_id)
                if amenity:
                    place.add_amenity(amenity)

        return True  # Return True to indicate success as per API requirements
