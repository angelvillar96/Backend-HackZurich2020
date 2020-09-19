from app import app
from flask import jsonify

@app.route('/', methods=['GET'])
def home():
    return "Hello world"


@app.route('/create_user', methods=['POST'])
def create_user():
    """
        Create a user

        data = [{
            name: <Name of user>,
            username: <Username (unique)>,
            calories: <Calories user wants to eat>,
            restrictions: <Food restrictions user has>
        }]

    """

    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()

    if user != None:
        return jsonify(
            message="Username already taken"
        ), 409
    else:
        user = User(username=data["username"], name=data["name"], calories=data["calories"])
        db.session.add(user)
        db.session.commit()
        return jsonify(
            message="User created succesfully"
        ), 200
