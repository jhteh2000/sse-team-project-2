import functions.database_functions as db

TEST_LOGIN_VALID = {"email": "test@email.com", "password": "test123"}
TEST_LOGIN_INVALID_EMAIL = {"email": "faketest@email.com", "password": "test123"}
TEST_LOGIN_INVALID_PASSWORD = {"email": "test@email.com", "password": "321tset"}

def test_index_page(client):
    response = client.get("/")
    # Will return index page with FoodHub header1
    assert response.status_code == 200
    assert b"<h1>FoodHub</h1>" in response.data

def test_food_finder_page(client):
    # Will return food finder page with ChooseYourMeal header1
    response = client.get("/foodfinder")
    assert response.status_code == 200
    assert b"<h1>Choose Your Meal</h1>" in response.data

def test_group_page_user_not_authenticated(client):
    response = client.get("/user-groups", follow_redirects=True)
    assert response.status_code == 200
    assert len(response.history) == 1
    assert response.request.path == "/login"

def test_login_page_user_not_authenticated(client):
    # Will return login page with Login header2
    response = client.get("/login")
    assert response.status_code == 200
    assert b"<h2>Login</h2>" in response.data

def test_login_page_user_login_with_valid_credentials(client):
    # Will redirect user to index page after login successfully
    response = client.post("/login", data=TEST_LOGIN_VALID, follow_redirects=True)
    assert response.status_code == 200
    assert len(response.history) == 1
    assert response.request.path == "/"

def test_login_page_user_login_with_invalid_email(client):
    # Will return login page with User Not Found error message
    response = client.post("/login", data=TEST_LOGIN_INVALID_EMAIL)
    assert response.status_code == 200
    assert b"<h2>Login</h2>" in response.data
    assert b"User Not Found" in response.data

def test_login_page_user_login_with_invalid_password(client):
    # Will return login page with Incorrect Password error message
    response = client.post("/login", data=TEST_LOGIN_INVALID_PASSWORD)
    assert response.status_code == 200
    assert b"<h2>Login</h2>" in response.data
    assert b"Incorrect Password" in response.data

def test_login_page_user_is_authenticated(client):
    # User logged in
    client.post("/login", data=TEST_LOGIN_VALID)

    # Will redirect user to login page if attempted to access login page again
    response = client.get("/login", follow_redirects=True)
    assert response.status_code == 200
    assert len(response.history) == 1
    assert response.request.path == "/"

def test_register_page(client):
    # Will return login page with Login header2
    response = client.get("/register")
    assert response.status_code == 200
    assert b"<h2>FoodHub - Register</h2>" in response.data

def test_user_registration_and_login_with_unused_email(client):
    # Will return registration success page with Registration Successful! header2
    new_user_info = {"firstName": "Fname", "lastName": "Lname", "email": "user1@test.com", "password": "test123"}
    response = client.post("/register", data=new_user_info)
    assert response.status_code == 200
    assert b"<h2>Registration Successful!</h2>" in response.data

    # Will be able to login using the newly registered credentials
    new_user_login = {"email": "user1@test.com", "password": "test123"}
    response = client.post("/login", data=new_user_login, follow_redirects=True)
    assert response.status_code == 200
    assert len(response.history) == 1
    assert response.request.path == "/"

    # Cleaning up from database
    db.delete_user_info("user1@test.com")

def test_user_registration_with_existing_email(client):
    new_user_info = {"firstName": "Fname", "lastName": "Lname", "email": "user1@test.com", "password": "test123"}
    
    # First registration
    client.post("/register", data=new_user_info)

    # Second registration with same registration details
    # Will return register page with email taken error message
    response = client.post("/register", data=new_user_info)
    assert response.status_code == 200
    assert b"<h2>FoodHub - Register</h2>" in response.data
    assert b"The email has already been taken" in response.data

    # Cleaning up from database
    db.delete_user_info("user1@test.com")

def test_logout_user_user_is_authenticated(client):
    # User logged in
    client.post("/login", data=TEST_LOGIN_VALID)

    # Will redirect user to index page
    response = client.get("/logout", follow_redirects=True)
    assert response.status_code == 200
    assert len(response.history) == 1
    assert response.request.path == "/"
