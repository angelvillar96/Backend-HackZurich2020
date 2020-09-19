from app import app, db
from flask import jsonify, request
from app.models import User, Food
from app.processing.api_requests import get_food_name

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
            restrictions: <Food restrictions user has>
        }

    """

    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()

    if user:
        return jsonify(
            message="Username already taken"
        ), 409
    else:
        user = User(username=data["username"], name=data["name"], calories=data["calories"])
        user.set_password(data["password"])
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

    data = request.get_json()
    user = User.query.filter_by(username=data["username"])

    if user:
        response = get_food_name(data["image"])
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

    data = request.get_json()
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
        data = [{
            date_consumed: <Data when food was consumed> (fromat: DD/MM/YY),
            payload: <Food that was consumed on that day>
        }]

    """
