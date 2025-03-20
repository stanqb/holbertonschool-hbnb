from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity

api = Namespace('reviews', description='Review operations')

# Define the review model for input validation and documentation
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(
        required=True,
        description='Rating of the place (1-5)'
    ),
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
})


@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(401, 'Authentication required')
    @api.response(403, 'Permission denied')
    @jwt_required()
    def post(self):
        """Register a new review (requires authentication)"""
        # Get current user from JWT token
        current_user = get_jwt_identity()

        # Get request data
        review_data = api.payload

        # Set user_id to current user's id if not admin
        if not current_user.get('is_admin', False):
            review_data['user_id'] = current_user.get('id')

        # Manual validation of the data
        errors = []

        # Validate text
        if not review_data.get('text') or review_data['text'].strip() == "":
            errors.append("Review text cannot be empty")

        # Validate rating
        try:
            rating = int(review_data.get('rating', 0))
            if not (1 <= rating <= 5):
                errors.append("Rating must be an integer between 1 and 5")
        except (ValueError, TypeError):
            errors.append("Rating must be an integer between 1 and 5")

        # Validate user_id and place_id
        if not review_data.get('user_id'):
            errors.append("User ID cannot be empty")

        if not review_data.get('place_id'):
            errors.append("Place ID cannot be empty")

        # Verify user and place exist if possible
        try:
            if not facade.get_user(review_data.get('user_id')):
                errors.append("Invalid user_id - user not found")
        except Exception:
            errors.append("Invalid user_id - user not found")

        try:
            if not facade.get_place_by_id(review_data.get('place_id')):
                errors.append("Invalid place_id - place not found")
        except Exception:
            errors.append("Invalid place_id - place not found")

        # Return errors if any
        if errors:
            return {'error': 'Invalid input data', 'details': errors}, 400

        try:
            # Create review using the facade
            review = facade.create_review(review_data)
            return review.to_dict(), 201
        except ValueError as e:
            api.abort(400, str(e))

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews"""
        # Get all reviews using the facade
        reviews = facade.get_all_reviews()
        return [review.to_dict() for review in reviews], 200


@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        # Get review by ID
        review = facade.get_review(review_id)

        if not review:
            api.abort(404, f"Review with id {review_id} not found")

        return review.to_dict(), 200

    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    @api.response(401, 'Authentication required')
    @api.response(403, 'Permission denied')
    @jwt_required()
    def put(self, review_id):
        """Update a review's information (requires authentication)"""
        # Get current user from JWT token
        current_user = get_jwt_identity()

        # Get the review
        review = facade.get_review(review_id)

        if not review:
            api.abort(404, f"Review with id {review_id} not found")

        # Check if user is the author of the review or an admin
        if (review.user_id != current_user.get('id') and
                not current_user.get('is_admin', False)):
            return {
                'error': (
                    'Permission denied. You can only update your own reviews'
                )
            }, 403

        # Get update data
        update_data = api.payload

        # Don't allow updating user_id or place_id
        if 'user_id' in update_data:
            del update_data['user_id']
        if 'place_id' in update_data:
            del update_data['place_id']

        # Manual validation of the update data
        errors = []

        # Validate text if provided
        if 'text' in update_data:
            if not update_data['text'] or update_data['text'].strip() == "":
                errors.append("Review text cannot be empty")

        # Validate rating if provided
        if 'rating' in update_data:
            try:
                rating = int(update_data['rating'])
                if not (1 <= rating <= 5):
                    errors.append("Rating must be an integer between 1 and 5")
            except (ValueError, TypeError):
                errors.append("Rating must be an integer between 1 and 5")

        # Return errors if any
        if errors:
            return {'error': 'Invalid input data', 'details': errors}, 400

        try:
            # Update review
            updated_review = facade.update_review(review_id, update_data)
            return updated_review.to_dict(), 200
        except ValueError as e:
            api.abort(400, str(e))

    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    @api.response(401, 'Authentication required')
    @api.response(403, 'Permission denied')
    @jwt_required()
    def delete(self, review_id):
        """Delete a review (requires authentication)"""
        # Get current user from JWT token
        current_user = get_jwt_identity()

        # Get the review
        review = facade.get_review(review_id)

        if not review:
            api.abort(404, f"Review with id {review_id} not found")

        # Check if user is the author of the review or an admin
        if (review.user_id != current_user.get('id') and
                not current_user.get('is_admin', False)):
            return {
                'error': (
                    'Permission denied. You can only delete your own reviews'
                )
            }, 403

        try:
            # Delete review
            facade.delete_review(review_id)
            return {"message": "Review deleted successfully"}, 200
        except ValueError as e:
            api.abort(400, str(e))


@api.route('/places/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        try:
            # Get reviews for place
            reviews = facade.get_reviews_by_place(place_id)
            return [review.to_dict() for review in reviews], 200
        except ValueError as e:
            api.abort(404, str(e))
