from app import db
import uuid
from datetime import datetime


class BaseModel(db.Model):
    __abstract__ = True  # This ensures SQLAlchemy does not create a table
    # for BaseModel
    id = db.Column(
        db.String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    def save(self):
        """Updates the modification timestamp and saves to the database"""
        self.updated_at = datetime.utcnow()
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        """Updates the object's attributes based on the provided dictionary"""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()
