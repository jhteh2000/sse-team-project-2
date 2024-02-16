import requests
import supabase
import os

# Constants for Supabase URL and API keys
SUPABASE_URL = os.getenv("SUPABASE_URL", "https://yydcqovanzimrbpfmfue.supabase.co")
AUTH_API_KEY = os.getenv("SUPABASE_API_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inl5ZGNxb3ZhbnppbXJicGZtZnVlIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTcwMTI2Mjk5NywiZXhwIjoyMDE2ODM4OTk3fQ.WTHLhx4Djm9jf5c5JuNhRc915ZX_BIg1xdittVKB_sI")

# Initialize the Supabase Client
supabase_client = supabase.create_client(SUPABASE_URL, AUTH_API_KEY)

# Headers for HTTP requests
HEADERS = {
    "apikey": AUTH_API_KEY,
    "Authorization": "Bearer " + AUTH_API_KEY,
    "Content-Type": "application/json",
}


########################################
##########       Tables       ##########
########################################
# LoginInfo: user_id (auto-gen), first_name, last_name, user_name (email), password
# Favorites: id (auto-gen), user_name (email), cuisine_name


# Functions
def get_data_from_table(table_name):
    """Fetch data from a Supabase table."""
    response = requests.get(f"{SUPABASE_URL}/rest/v1/{table_name}", headers=HEADERS)
    if response.status_code == 200:
        print("Request success!")
        return response.json()
    else:
        return f"Error: {response.text}"



def add_row_to_table(table_name, data_to_insert):
    """Insert a new row into a Supabase table."""
    data, _ = supabase_client.table(table_name).insert([data_to_insert]).execute()
    return data

def delete_row_from_table(table_name,  username, uri):
    """Delete a row from the Supabase table."""
    data, _ = (
            supabase_client.table(table_name)
            .delete()
            .eq("username (email)", username)
            .eq("dish_uri", uri)
            .execute()
    )
    return data

def return_data(table_name, username):
    """Return data based on username from a Supabase table."""
    data, _ = (
        supabase_client.table(table_name)
        .select("*")
        .eq("username (email)", username)
        .execute()
    )
    return data[1]

def return_user(id):
    """Return data based on username from a Supabase table."""
    data, _ = (
        supabase_client.table("LoginInfo")
        .select("*")
        .eq("id", id)
        .execute()
    )
    return data[1]


def print_user_info(user_data, width=20):
    """Print user information in a formatted way."""
    user_FirstName = user_data["first_name"]
    user_LastName = user_data["last_name"]
    user_UserName = user_data["username (email)"]

    print("First Name:".ljust(width) + user_FirstName)
    print("Last Name:".ljust(width) + user_LastName)
    print("Username (Email):".ljust(width) + user_UserName)
    print()


def print_favorites_info(favorites_data, width=20):
    """Print favorite cuisine information."""
    for item in favorites_data:
        user_USERNAME = item["username (email)"]
        user_CUISINE = item["cuisine_name"]

        print("Username (Email):".ljust(width) + user_USERNAME)
        print("Cuisine Name:".ljust(width) + user_CUISINE)
        print()


# TODO: A function to return user_FirstName, user_LastName, user_UserName
# TODO: A function to return list of {user_USERNAME, user_CUISINE}


########################################
##########     Execution      ##########
########################################

username_to_check = "test@email.com"

# Example usage: LoginInfo
# user_data = return_data("LoginInfo", username_to_check)
# print()
# print(user_data)
# if user_data:
#     print("User information:")
#     print_user_info(user_data[0])

# Example usage: Favorites
favorites_data = return_data("Favorites", username_to_check)
# delete_row_from_table("Favorites", username_to_check, "http://www.edamam.com/ontologies/edamam.owl#recipe_92f5af46a5adafda4b26ff16f4fb7c89")
print(favorites_data)
# if favorites_data:
#     print("Favorite cuisines:")
#     print_favorites_info(favorites_data)

# data_to_insert - Interface where interact with register page when submit
# new_user_FIRSTNAME = "Test_name2"
# new_user_LASTNAME = "Test_lastname2"
# new_user_USERNAME = "Test_email2"
# new_user_PASSWORD = "Test_password2"

# new_user_data = {
#     "first_name": new_user_FIRSTNAME,
#     "last_name": new_user_LASTNAME,
#     "username (email)": new_user_USERNAME,
#     "password": new_user_PASSWORD
# }

#Example useage: Delete Row
# test5_data = return_data("Favorites", 'test5@email.com')
# print(test5_data)

#delete_row_from_table("Favorites", 'test5@email.com', 'http://www.edamam.com/ontologies/edamam.owl#recipe_4bb99424e1bbc40d3cd1d891883d6745')


