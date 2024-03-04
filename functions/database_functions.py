from dotenv import load_dotenv 
import supabase
import os

load_dotenv()

# Constants for Supabase URL and API keys
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Initialize the Supabase Client
supabase_client = supabase.create_client(SUPABASE_URL, SUPABASE_KEY)

def fetch_user_info(email):
    data, count = supabase_client.table("User Registration").select("*").eq("email", email).execute()

    return data[1]

def insert_user_info(new_user_info):
    """
    new_user_info example:
    new_user_info = {
        "email": email,
        "firstname": firstName,
        "lastname": lastName,
        "password": generate_password_hash(password),
    }
    """
    data, count = supabase_client.table("User Registration").insert(new_user_info).execute()
