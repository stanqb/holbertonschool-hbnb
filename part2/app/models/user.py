#!/usr/bin/python3
class User:
    """counter to to generate unique id""" 
    id_counter = 1
    def __init__(self, first_name, last_name, email,):
        self.id = User.id_counter
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        User.id_counter += 1
        
    def update(self, data):
        """updating users informations"""
        self.first_name = data.get('first_name', self.first_name)
        self.last_name = data.get('last_name', self.last_name)
        self.email = data.get('email', self.email)