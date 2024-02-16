import os
import requests
import supabase

def test_edamam_api_status():
    edamam_api = (
        "https://api.edamam.com/api/recipes/v2/?type=public&app_id="
        + os.getenv("EDAMAM_APP_ID")
        + "&app_key="
        + os.getenv("EDAMAM_APP_KEY")
    )
    response = requests.get(edamam_api)
    assert response.status_code == 200

def test_supabase_api_status():
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    AUTH_API_KEY = os.getenv("SUPABASE_AUTH_API_KEY")

    HEADERS = {
        "apikey": AUTH_API_KEY,
        "Authorization": "Bearer " + AUTH_API_KEY,
        "Content-Type": "application/json",
    }

    response = requests.get(f"{SUPABASE_URL}/rest/v1/LoginInfo", headers=HEADERS)
    
    assert response.status_code == 200