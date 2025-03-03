from flask_restx import Namespace, Resource, fields
from app.services import facade

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
    def post(self):
        """Register a new review"""
        # Get request data
        review_data = api.payload

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
    def put(self, review_id):
        """Update a review's information"""
        # Get the review
        review = facade.get_review(review_id)

        if not review:
            api.abort(404, f"Review with id {review_id} not found")

        # Get update data
        update_data = api.payload

        # Don't allow updating user_id or place_id
        if 'user_id' in update_data:
            del update_data['user_id']
        if 'place_id' in update_data:
            del update_data['place_id']

        try:
            # Update review
            updated_review = facade.update_review(review_id, update_data)
            return updated_review.to_dict(), 200
        except ValueError as e:
            api.abort(400, str(e))

    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        """Delete a review"""
        # Get the review
        review = facade.get_review(review_id)

        if not review:
            api.abort(404, f"Review with id {review_id} not found")

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
