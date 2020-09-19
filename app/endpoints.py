from app import app, db
from flask import jsonify, request
from app.models import User, Food
from app.processing.api_requests import get_food_name, get_recipes_by_ingredient
from app.processing.utils import process_overview
from app.processing.filter_recipes import filter_sort_recipes


@app.route('/', methods=['GET'])
def home():
    return "Hello world"


@app.route('/api/create_user', methods=['POST'])
def create_user():
    """
        Create a user

        expects:
        {
            name: <Name of user>,
            username: <Username (unique)>,
            password: <Password>,
            calories: <Calories user wants to eat>,
            restrictions: [
                {type: lactose_intolerant, bool: <True or False>},
                {type: low_carb, bool: <True or False>},
                {type: vegan, bool: <True or False>},
                {type: vegetarian, bool: <True or False>}
            ]
        }

    """

    data = request.form
    user = User.query.filter_by(username=data['username']).first()

    if user:
        return jsonify(
            message="Username already taken"
        ), 409
    else:
        user = User(username=data["username"], name=data["name"], calories=data["calories"])
        user.set_password(data["password"])
        rest = data["restrictions"]
        for r in rest:
            if r["type"] == "lactose_intolerant" and r["bool"] == "True":
                user.lactose_intolerant = True
            elif r["type"] == "vegan" and r["bool"] == "True":
                user.vagan = True
            elif r["type"] == "vegetarian" and r["bool"] == "True":
                user.vegetarian = True
            elif r["type"] == "low_carb" and r["bool"] == "True":
                user.lactose_intolerant = True

        db.session.add(user)
        db.session.commit()
        return jsonify(
            message="User created succesfully",
            username=data["username"]
        ), 200


@app.route('/api/process_food', methods=['POST'])
def check_food():
    """
        Processes the image and returns suggestion for food

        expects:
        {
            username: <Username> (used for authentification),
            image: <Image of food> (in base64)
        }

        returns:
        {
            data: [{
                calories: <Calories of food>,
                amount: <Amount of food in grams>,
                name: <Name of food>
                nutrition: {
                    total_fat: <Amount fat>,
                    protein: <Amount protein>,
                    ...
                }
            }],
            message: "Processing successful"
        }

    """
    data = request.form
    if data == None:
        return jsonify(
            message="No data"
        ), 404

    user = User.query.filter_by(username=data["username"])

    if user:
        response = get_food_name(data["image"])
        print(response)
        return jsonify(
            message="Processing successful",
            data=response
        ), 200
    else:
        return jsonify(
            message="Not Authorized"
        ), 401

@app.route('/api/confirm_food', methods=['POST'])
def confirm_food():
    """
        User confirms food and it gets added to database

        expects:
        {
            username: <Username> (used for authentification),
            date_consumed: <Data when food was consumed> (fromat: DD/MM/YY),
            payload: <Data that was sent to confirm>
        }

    """

    data = request.form
    user = User.query.filter_by(username=data["username"]).first()

    if user:
        food = Food(name=data["payload"]["name"], date_consumed=data["date_consumed"], calories=data["payload"]["nutrition"]["calories"], fat=data["payload"]["nutrition"]["total_fat"], protein=data["payload"]["nutrition"]["protein"], sugar=data["payload"]["nutrition"]["sugars"], carbs=data["payload"]["nutrition"]["total_carb"], sodium=data["payload"]["nutrition"]["sodium"], consumer=user)
        db.session.add(food)
        db.session.commit()
        return jsonify(
            message="Food added successfully"
        ), 200
    else:
        return jsonify(
            message="Not Authorized"
        ), 401

@app.route('/api/overview/<username>/<date>', methods=['GET'])
def overview(username, date):
    """
        Overview of a users diet on a specific date

        returns
        {
            date_consumed: <Data when food was consumed> (fromat: DD.MM.YY as string),
            foods: [
                {
                    name: <Name of food>,
                    calories: <Calories of food>,
                    fat: <Amount of fat in grams>,
                    carbs: <Amount of carbs in grams>,
                    protein: <Amount of protein in grams>
                },
                ...
            ],
            total_calories: <Calories from all foods eaten on the specific date>,
            total_fat: <Amount of fat eaten on the specific date>,
            total_protein: <Amount of protein eaten on the specific date>,
            total_carbs: <Amount of carbs eaten on the specific date>,
            progress: <Percent of total calories>
        }

    """
    user = User.query.filter_by(username=username).first()
    data = process_overview(user, date) #returns list with all foods eaten on the specific date
    return jsonify(
        data=data
    ), 200

@app.route('/api/get_recipe', methods=['POST'])
def get_recipe():
    """
        Gives the user a list of recommendations based on an ingredient

        expects
        {
            username: <Username>,
            ingredient: <Ingredient>
        }

        returns
        {
            recommendations: <List of recommendations sorted from best to worst>
        }

    """
    data = request.form
    user = User.query.filter_by(username=data["username"]).first()

    if user:
        recommendations = get_recipes_by_ingredient(data["ingredient"])

        filtered = recommendations#filter_sort_recipes(recommendations, user)
        return jsonify(
            recommendations=filtered
        ), 200
    else:
        return jsonify(
            message="Not Authorized"
        ), 401

@app.route('/api/profile/<username>', methods=['GET'])
def profile(username):

    user = User.query.filter_by(username=username).first()
