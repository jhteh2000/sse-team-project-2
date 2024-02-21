from flask import Flask, render_template, redirect, url_for
from dotenv import load_dotenv
import os
from flask_login import LoginManager

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
    return render_template("group.html")

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
    return redirect(url_for("index"))