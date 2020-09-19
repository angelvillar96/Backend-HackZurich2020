"""
Methods for sorting and filtering the recipes based on dietary restrictions
and passed user behavior
"""

from config import Config


def filter_sort_recipes(recipes, username):
    """
    Filtering/sorting the retrieved recipes based on the dietary
    restrictions of a user
    """

    # obtaining the restiriction values for the current user
    restrictions = _get_restictions(username=username)
    user = User.query.filter_by(username=username).first()

    filtered_recipes = _filter_recipes(recipes=recipes, user=user)
    sorted_recipes = _sort_recipes(recipes=filtered_recipes, user= user)

    return


def _filter_recipes(recipes, user):
    """
    Filtering recipes based on the dietary restrictions of the user
    """

    # filtering recipes that do not compeil with the
    filtered_recipes = []
    for recipe in recipes:
        # excluding recipes that do not compeil with the dietary restrictions
        if(("Vegan" not in recipe["nutrition_type"] and user.restrictions.vegan is True):
            continue
        if(("Vegetarish" not in recipe["nutrition_type"]and user.restrictions.vegetarian is True):
            continue
        if(("Milchprodukte" not in recipe["allergens"] and user.restrictions.lactose_intolerant is True):
            continue

        # excluding recipes that do not compeil with the low-carb threshold
        carbs = recipe["general_info"]["nutrition"]["carbohydrates_percent"]
        if(carbs > Config.LOW_CARB_THR and user.restrictions.low_carb is True):
            continue

        # excluding recipes with allergens
        allergens = user.restrictions.allergens
        recipe_allergens = recipe["allergens"]
        # if length of joined list with removing duplicate smaller than sum of lengths
        if( len(list(set(recipe_allergens + allergens))) < len(allergens) + len(recipe_allergens)):
            continue
        filtered_recipes.append(recipe)

    return filtered_recipes


def _sort_recipes(recipes, user):
    """
    Sorting the recipes based on some helth-based value
    """

    return recipes



def _get_restictions(username):
    """
    Getting the dietary restrictions of a user
    """

    user = User.query.filter_by(username=username).first()
    restrictions = {
        "vegetarian": user.vegetarian,
        "vegan": user.vegan,
        "lactose_intolerant": user.lactose_intolerant,
        "low_carb": user.low_carb
    }

    return restrictions
