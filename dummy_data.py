from app.models import User, Food
from app import db

user0 = User(username="test", name="Test", achievements="1,2,4", password_hash="123", calories=2000, low_carb=True)
user1 = User(username="theo", name="Theo", achievements="1,3", password_hash="123", calories=2800, vegetarian=True)
user2 = User(username="mike", name="Mike", achievements="4", password_hash="123", calories=2200, low_carb=True)
user3 = User(username="luca", name="Luca", achievements="2,3,6", password_hash="123", calories=3000)
user4 = User(username="philip", name="Philip", achievements="5", password_hash="123", calories=2500, vegan=True)
user5 = User(username="silvan", name="Silvan", achievements="1", password_hash="123", calories=2200, lactose_intolerant=True)

db.session.add(user0)
db.session.add(user1)
db.session.add(user2)
db.session.add(user3)
db.session.add(user4)
db.session.add(user5)

db.session.commit()
