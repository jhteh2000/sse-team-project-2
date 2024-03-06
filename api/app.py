from flask import Flask, render_template, redirect, url_for, request, jsonify
from dotenv import load_dotenv
import os
from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required,
    current_user,
)
import json
import requests
from functions.database_functions import fetch_user_info
from functions.userclass import User
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta
from postgrest.exceptions import APIError
from functions.database_functions import insert_user_info, insert_user_favorites, delete_user_favorites

load_dotenv()

# Flask app configuration
app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")

# Setting up flask login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(email):
    return User.get(email)


@app.route("/")
def index():
    return render_template("index.html")


# Food finder page
@app.route("/food")
def food():
    return render_template("foodfinder.html")


# The form submitted in the food page will go to this route
@app.route("/food/submit", methods=["POST"])
def submit():
    # Retrieve the form value and add into a dictionary
    args = {}
    args["dishname"] = request.form.get("dishname")
    args["diet"] = request.form.getlist("diet")
    args["health"] = request.form.getlist("health")
    args["cuisine"] = request.form.getlist("cuisine")
    args["dish"] = request.form.getlist("dish")

    response = requests.post("http://127.0.0.1:4000", json=args)

    if response.status_code == 200:
        return redirect(url_for("foodSearchResults", data=response.text))


# Food finder search results page
@app.route("/food/results")
def foodSearchResults():
    data = json.loads(request.args.get("data"))

    return render_template("results.html", result_args=data)

@app.route("/user-groups")
def user_groups():
    user_email = 'user1@gmail.com' # Need to change to current_user.email in production
    try:
        server_url = "http://127.0.0.1:3000/display-user-groups"
        payload = {'userEmail': user_email}
        headers = {'Content-Type': 'application/json'}

        print(f'Sending request to {server_url} with payload: {payload}')
        response = requests.post(server_url, json=payload, headers=headers)
        response.raise_for_status()

        groups_data = response.json()
        print(f'Received response: {groups_data}')

        return render_template("user_groups.html", groups=groups_data, userEmail=user_email)
    except requests.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        return f"HTTP error occurred: {http_err}", 500
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return f"An error occurred: {str(e)}", 500

@app.route("/group-info")
def group_info():
    group_name = request.args.get('group_name')
    group_id = request.args.get('group_id')
    try:
        # Define the server URLs
        members_url = "http://127.0.0.1:3000/display-group-members"
        votes_url = "http://127.0.0.1:3000/display-top-votes"

        # Set the payload to include group_id or group_name depending on your API
        payload_members = {'groupId': group_id}
        payload_votes = {'groupId': group_id}
        headers = {'Content-Type': 'application/json'}

        # Make requests to the server
        response_members = requests.post(members_url, json=payload_members, headers=headers)
        response_votes = requests.post(votes_url, json=payload_votes, headers=headers)

        # Raise an exception if there was an error with the request
        response_members.raise_for_status()
        response_votes.raise_for_status()

        # Extract the data from the responses
        members_data = response_members.json()
        votes_data = response_votes.json()

        print("Members data received:", members_data)
        print("Votes data received:", votes_data)

        # Render the template and pass the data
        return render_template("group_info.html", group_name=group_name, group_id=group_id, members_info=members_data, votes_info=votes_data)

    except requests.HTTPError as http_err:
        # If there is an HTTPError, return the error message
        print("HTTP error occurred:", http_err)
        return f"HTTP error occurred: {http_err}", 500
    except Exception as e:
        # For other exceptions, print and return the error message
        print("Error:", str(e))
        return f"An error occurred: {str(e)}", 500


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated is False:
        if request.method == "POST":
            email = request.form.get("email")
            password = request.form.get("password")
            
            # Retrieve user data from the database
            user_data = fetch_user_info(email)
            
            if user_data:
                user = User(user_data[0]['email'], user_data[0]['firstname'], user_data[0]['lastname'], user_data[0]['password'])

                if check_password_hash(user.password, password):
                    login_user(user, remember=True, duration=timedelta(weeks=1))
                    next = request.args.get("next")
                    return redirect(next or url_for("index"))
                
                # Return incorrect password error message if password hash does not match
                return render_template("login.html", error="Incorrect Password")
            
            # Return user not found error message if email is not in database
            return render_template("login.html", error="User Not Found")
        
        # Default login page if using HTTP GET method
        return render_template("login.html")
    else:
        # Redirect to homepage if authenticated user attempted to login again
        return redirect(url_for("index"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        firstName = request.form.get("firstName")
        lastName = request.form.get("lastName")
        email = request.form.get("email")
        password = request.form.get("password")

        new_user_info = {
            "email": email,
            "firstname": firstName,
            "lastname": lastName,
            "password": generate_password_hash(password),
        }

        # The database will raise APIError exception if the email is taken as it will violate the primary key rule
        try:
            insert_user_info(new_user_info)
        except APIError:
            return render_template("register.html", error="The email has already been taken")

        return render_template("registration_success.html", name=firstName)
    
    # Default register page if using HTTP GET method
    return render_template("register.html")


@app.route("/profile")
@login_required
def profile():
    favorites_placeholder = {"count": 0}
    return render_template("profile.html", favorites=favorites_placeholder)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))

@app.route("/add_selected_food", methods=['POST'])
@login_required
def add_selected_food():
    try:
        data = request.get_json()
        insert_user_favorites(current_user.email, data["uri"])

        return jsonify({'message': 'Food item added successfully'})
    except Exception as e:
        return jsonify({'error': 'Failed to add food item'}), 500

@app.route("/remove_selected_food", methods=['POST'])
@login_required
def remove_selected_food():
    try:
        data = request.get_json()
        delete_user_favorites(current_user.email, data["uri"])

        return jsonify({'message': 'Food item removed successfully'})
    except Exception as e:
        return jsonify({'error': 'Failed to remove food item'}), 500

@app.route("/vote")
def vote():
    return render_template("vote.html")
