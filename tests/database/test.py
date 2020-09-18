from app.models import User, Food
from app import db


#create User
try:
    user = User(username="test", name="Text", password_hash="123")
    db.session.add(user)
    db.session.commit()
    print("Create User successful")
except:
    print("Create User failed")

#add food
try:
    food = Food(name="Hot Dog", calories=280, fat=20, carbs=30, protein=10, sugar=5, sodium=10, consumer=user.user_id)
    db.session.add(food)
    db.session.commit()
    print("Add Food successful")
except:
    print("Add Food failed")
