from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import json
from functions.results import process_search, get_response_recipe, get_response_uri
from functions.userbaseAPI import add_row_to_table, return_data, return_user, delete_row_from_table
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from functions.userclass import User
from datetime import timedelta
from os.path import join
from postgrest.exceptions import APIError
import os
import json

# Flask app configuration
app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "icptrlAM4HuEBWdcsHDBqedr9dOxeX72")

# Setting up flask login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login" # redirect the user to login route if the page requires a logged-in user

@login_manager.user_loader
def load_user(user_id):
    user_data = return_user(user_id)
    if user_data:
        user = User(user_data[0]['id'], user_data[0]['first_name'], user_data[0]['last_name'], user_data[0]['username (email)'], user_data[0]['password'])
    else:
        user = None
    return user

# All flask routes
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/submit", methods=["POST"])
def submit():
    args = {}
    args["dishname"] = request.form.get("dishname")
    args["diet"] = request.form.getlist("diet")
    args["health"] = request.form.getlist("health")
    args["cuisine"] = request.form.getlist("cuisine")
    args["dish"] = request.form.getlist("dish")

    return redirect(url_for("results", args_dict=json.dumps(args)))


@app.route("/results")
def results():
    # Retrieve args_dict from the URL parameters and convert JSON string to dict
    args_dict = request.args.get("args_dict")
    args_dict = json.loads(args_dict)

    # For Testing (Will be replaced with Requests)
    # with open(join("../samplejson", "recipe.json"), "r") as read_file:
    #     data = json.load(read_file)

    # For Production
    response = get_response_recipe(args_dict)
    data = response.json()

    result_args = {
        "count": 0,
        "uri": [],
        "image": [],
        "name": [],
        "calories": [],
        "protein": [],
        "ingredient": [],
        "recipeURL": [],
    }

    for recipe in data["hits"]:
        if process_search(args_dict, recipe):
            result_args["uri"].append(recipe["recipe"]["uri"])
            result_args["image"].append(recipe["recipe"]["image"])
            result_args["name"].append(recipe["recipe"]["label"])
            result_args["calories"].append(
                round(
                    recipe["recipe"]["totalNutrients"]["ENERC_KCAL"]["quantity"],
                    ndigits=3,
                )
            )
            result_args["protein"].append(
                round(
                    recipe["recipe"]["totalNutrients"]["PROCNT"]["quantity"], ndigits=3
                )
            )
            result_args["ingredient"].append(recipe["recipe"]["ingredientLines"])
            result_args["recipeURL"].append(recipe["recipe"]["url"])
            result_args["count"] += 1

    # Favorite list check, if user has logged in, and the dish is already in list, heart remains red
    favorites = []
    if current_user.is_authenticated is True:
        for dish in return_data("Favorites", current_user.email):
            favorites.append(dish["dish_uri"])

    return render_template("results.html", result_args=result_args, favorites=favorites)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated is False:
        if request.method == "POST":
            email = request.form.get("email")
            password = request.form.get("password")
            
            # Retrieve user data from the database
            user_data = return_data("LoginInfo", email)
            if user_data:
                user = User(user_data[0]['id'], user_data[0]['first_name'], user_data[0]['last_name'], user_data[0]['username (email)'], user_data[0]['password'])
                if check_password_hash(user.password, password):
                    login_user(user, remember=True, duration=timedelta(days=1))
                    next = request.args.get("next")
                    return redirect(next or url_for("index"))
                return render_template("login.html", error="Incorrect Password")
            return render_template("login.html", error="User Not Found")
        return render_template("login.html")
    else:
        return redirect(url_for("index"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        firstName = request.form.get("firstName")
        lastName = request.form.get("lastName")
        email = request.form.get("email")
        password = request.form.get("password")

        data_to_insert = {
            "first_name": firstName,
            "last_name": lastName,
            "username (email)": email,
            "password": generate_password_hash(password),
        }

        try:
            add_row_to_table("LoginInfo", data_to_insert)
        except APIError:
            print("The email has been used")
            return render_template("register.html", error="The email has already been taken")

        return render_template("registration_success.html", name=firstName)
    return render_template("register.html")

@app.route("/user_info")
@login_required
def user_info():
    uri_list = []
    for dish in return_data("Favorites", current_user.email):
        uri_list.append(dish["dish_uri"])

    # For Testing (Will be replaced with Requests)
    # with open(join("../samplejson", "recipe.json"), "r") as read_file:
    #     data = json.load(read_file)

    favorites = {
        "count": 0,
        "uri": [],
        "image": [],
        "name": [],
        "calories": [],
        "protein": [],
        "ingredient": [],
        "recipeURL": [],
    }

    # # For Production
    response = get_response_uri(uri_list)
    if response.status_code == 200:  #Check if the response if successful 
        data = response.json()

        for recipe in data["hits"]:
            # TESTING ONLY (DELETE THIS IF STATEMENT FOR PRODUCTION)
            if recipe["recipe"]["uri"] in uri_list: 
                favorites["uri"].append(recipe["recipe"]["uri"])
                favorites["image"].append(recipe["recipe"]["image"])
                favorites["name"].append(recipe["recipe"]["label"])
                favorites["calories"].append(
                    round(
                        recipe["recipe"]["totalNutrients"]["ENERC_KCAL"]["quantity"],
                        ndigits=3,
                    )
                )
                favorites["protein"].append(
                    round(
                        recipe["recipe"]["totalNutrients"]["PROCNT"]["quantity"], ndigits=3
                    )
                )
                favorites["ingredient"].append(recipe["recipe"]["ingredientLines"])
                favorites["recipeURL"].append(recipe["recipe"]["url"])
                favorites["count"] += 1

    return render_template("userInfo.html", favorites=favorites)

@app.route("/choose")
@login_required
def choose():
    uri_list = []
    for dish in return_data("Favorites", current_user.email):
        uri_list.append(dish["dish_uri"])

    # For Testing (Will be replaced with Requests)
    # with open(join("../samplejson", "recipe.json"), "r") as read_file:
    #     data = json.load(read_file)

    favorites = {
        "count": 0,
        "uri": [],
        "image": [],
        "name": [],
        "calories": [],
        "protein": [],
        "ingredient": [],
        "recipeURL": [],
    }

    # # For Production
    response = get_response_uri(uri_list)
    if response.status_code == 200:  #Check if the response if successful 
        data = response.json()

        for recipe in data["hits"]:
            # TESTING ONLY (DELETE THIS IF STATEMENT FOR PRODUCTION)
            if recipe["recipe"]["uri"] in uri_list: 
                favorites["uri"].append(recipe["recipe"]["uri"])
                favorites["image"].append(recipe["recipe"]["image"])
                favorites["name"].append(recipe["recipe"]["label"])
                favorites["calories"].append(
                    round(
                        recipe["recipe"]["totalNutrients"]["ENERC_KCAL"]["quantity"],
                        ndigits=3,
                    )
                )
                favorites["protein"].append(
                    round(
                        recipe["recipe"]["totalNutrients"]["PROCNT"]["quantity"], ndigits=3
                    )
                )
                favorites["ingredient"].append(recipe["recipe"]["ingredientLines"])
                favorites["recipeURL"].append(recipe["recipe"]["url"])
                favorites["count"] += 1

    return render_template("userInfo.html", favorites=favorites)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You are logged out")
    return redirect(url_for("index"))

@app.route("/add_selected_food", methods=['POST'])
@login_required
def add_selected_food():
    try:
        data = request.get_json()
        data_to_insert = {
            "username (email)": current_user.email,
            "dish_uri": data["uri"]
        }
        add_row_to_table("Favorites", data_to_insert)

        return jsonify({'message': 'Food item added successfully'})
    except Exception as e:
        return jsonify({'error': 'Failed to add food item'}), 500

@app.route("/remove_selected_food", methods=['POST'])
@login_required
def remove_selected_food():
    try:
        data = request.get_json()
        dish_uri = data["uri"]

        # print(f"Removing food for username: {current_user.email}, uri: {dish_uri}")

        delete_row_from_table("Favorites", current_user.email, dish_uri)

        return jsonify({'message': 'Food item removed successfully'})
    except Exception as e:
        return jsonify({'error': 'Failed to remove food item'}), 500


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
