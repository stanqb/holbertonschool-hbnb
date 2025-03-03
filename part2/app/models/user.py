import uuid


class User:
    def __init__(self, first_name, last_name, email):
        self.id = str(uuid.uuid4())
        self.first_name = first_name
        self.last_name = last_name
        self.email = email

    def update(self, updated_data):
        self.first_name = updated_data.get('first_name', self.first_name)
        self.last_name = updated_data.get('last_name', self.last_name)
        self.email = updated_data.get('email', self.email)
