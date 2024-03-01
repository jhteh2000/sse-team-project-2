from flask import Flask, render_template, redirect, url_for, request
from dotenv import load_dotenv
import os
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
import json
import requests

load_dotenv()

# Flask app configuration
app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")

# Setting up flask login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login" 

@login_manager.user_loader
def load_user(user_id):
    # To be completed
    # user_data = return_user(user_id)
    # if user_data:
    #     user = User(user_data[0]['id'], user_data[0]['first_name'], user_data[0]['last_name'], user_data[0]['username (email)'], user_data[0]['password'])
    # else:
    #     user = None
    user = None
    return user


@app.route("/")
def index():
    return render_template("index.html")

# Food finder page
@app.route("/food")
def food():
    return render_template("food.html")

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

@app.route("/group")
def group():
    try:
        # Load group data from the JSON file (replace with your actual file path)
        with open("group.json", "r") as json_file:
            groups_data = json.load(json_file)

        # Print loaded data for debugging
        print("Loaded data:", groups_data)

        # Render the template and pass the data
        return render_template("group.html", groups=groups_data["groups"])

    except Exception as e:
        # Print any exception for debugging
        print("Error:", str(e))
        return "An error occurred."

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/profile")
def profile():
    favorites_placeholder = {"count": 0}
    return render_template("profile.html", favorites=favorites_placeholder)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))