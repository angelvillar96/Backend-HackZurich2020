"""
Methods for data processing and other common functionalities
"""
from app.models import User, Food

def process_overview(user, date):
    foods = user.foods.filter_by(date_consumed=date).all()

    food_list = []
    total_calories = 0
    total_fat = 0
    total_carbs = 0
    total_protein = 0
    for food in foods:
        dict = {
            'name': food.name,
            'calories': food.calories,
            'fat': food.fat,
            'carbs': food.carbs,
            'protein': food.protein
        }
        food_list.append(dict)
        total_calories += food.calories
        total_fat += food.fat
        total_carbs += food.carbs
        total_protein += food.protein

    if total_calories == 0:
        progress = 0
    else:
        progress = user.calories / total_calories * 100

    payload = {
        'date_consumed': date,
        'foods': food_list,
        'total_calories': total_calories,
        'total_carbs': total_carbs,
        'total_fat': total_fat,
        'total_protein': total_protein,
        'progress': progress
    }

    return payload
