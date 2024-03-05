from flask_login import UserMixin
from functions.database_functions import fetch_user_info

class User(UserMixin):
    def __init__(self, email, first_name, last_name, password):
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.selected_food_items = []

    def get_id(self):
        return self.email

    @classmethod
    def get(cls, email):
        user_data = fetch_user_info(email)
        if user_data:
            user = cls(user_data[0]['email'], user_data[0]['firstname'], user_data[0]['lastname'], user_data[0]['password'])
        else:
            user = None
        return user

    def add_selected_food_item(self, food_data):
        self.selected_food_items.append(food_data)

    def get_selected_food_items(self):
        return self.selected_food_items