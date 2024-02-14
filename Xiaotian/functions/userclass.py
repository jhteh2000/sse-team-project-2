from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id, first_name, last_name, email, password):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.selected_food_items = []

    def add_selected_food_item(self, food_data):
        self.selected_food_items.append(food_data)

    def get_selected_food_items(self):
        return self.selected_food_items
