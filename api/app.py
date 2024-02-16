from flask import Flask, render_template
from dotenv import load_dotenv
from flask_login import LoginManager

load_dotenv()

app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)

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
    return "Login"

@app.route("/register")
def register():
    return "Register"