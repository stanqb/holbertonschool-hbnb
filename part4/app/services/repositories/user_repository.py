from app.models.user import User
from app.persistence.repository import SQLAlchemyRepository


class UserRepository(SQLAlchemyRepository):
    """Repository for User model"""

    def __init__(self):
        super().__init__(User)

    def get_user_by_email(self, email):
        """Find a user by their email address"""
        return self.model.query.filter_by(email=email).first()

    def save(self):
        """Save changes to the database"""
        from app import db
        db.session.commit()
