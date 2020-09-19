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

        data = [{
            name: <Name of user>,
            username: <Username (unique)>,
            password: <Password>,
            calories: <Calories user wants to eat>,
            restrictions: <Food restrictions user has>
        }]

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

        data = [{
            username: <Username> (used for authentification),
            image: <Image of food> (in base64)
        }]

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
