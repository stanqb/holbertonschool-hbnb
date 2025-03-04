import uuid


class User:
    def __init__(self, first_name, last_name, email, password=None, **kwargs):
        self.id = str(uuid.uuid4())
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password

    def update(self, updated_data):
        self.first_name = updated_data.get('first_name', self.first_name)
        self.last_name = updated_data.get('last_name', self.last_name)
        self.email = updated_data.get('email', self.email)
        if 'password' in updated_data:
            self.password = updated_data['password']

    def to_dict(self):
        """Return a dictionary representation of the user"""
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email

        }
