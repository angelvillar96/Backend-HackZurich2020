"""
Testing the functionality of the API Requests processing libraries
"""

import os
import sys
import json
from PIL import Image
import base64

sys.path.append("..")
import app.processing.api_requests as api_requests
import app.processing.filter_recipes as filter_recipes


def test_get_food_name():
    """
    Testing that the results of the Bite Food Recognition System works fine
    """

    # img_path = os.path.join(os.getcwd(), "resources", "pizza.jpeg")
    img_path = os.path.join(os.getcwd(), "resources", "hot_dog.jpg")
    with open(img_path, "rb") as img:
        img_base64 = base64.b64encode(img.read())
    img_base64 = img_base64.decode("utf-8")

    products = api_requests.get_food_name(img_base64)

    return


def test_get_product_params():
    """
    """

    response = api_requests.get_product_by_name("salad")
    print(response)

    return


def test_get_recipes():
    """
    """

    # ingredient = api_requests.get_product_by_name("rice")
    recipes = api_requests.get_recipes_by_ingredient(ingredient=None, n_items=5)
    # filtered_recipes = filter_recipes(recipes=recipes, username="test")

    print(len(recipes))
    with open("recipes.json", "w") as f:
        json.dump(recipes, f)

    return



if __name__ == "__main__":
    os.system("clear")
    # test_get_food_name()
    # test_get_product_params()
    test_get_recipes()

#
