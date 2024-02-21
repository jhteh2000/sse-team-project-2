from flask import Flask, render_template
from dotenv import load_dotenv
import os
from flask_login import LoginManager
import json

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

@app.route("/food")
def food():
    return render_template("food.html")


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