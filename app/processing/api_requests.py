"""
Handling requests to Migros and Bite APIs for fetching data
"""

import json
import requests

from config import Config


def get_food_name(img, n_items=1):
    """
    Obtaining the food name and nutritious value from a porduct given an image
    of such food product. Uses Bite API
    Args:
    -----
    img:
    """

    api_key = Config.FOOD_RECOGNITION_KEY
    food_recognition_url = "https://api-beta.bite.ai/vision/"

    headers = {'Content-Type': 'application/json',
               'Authorization': 'Bearer {0}'.format(api_key)}
    data = {
        "base64": img
    }

    response = requests.post(food_recognition_url, json=data, headers=headers)
    response = response.json()

    n_detections = len(response["items"])
    products = []
    # processing product information for each detection from the neural net
    for i in range(n_items):
        detected_item = response["items"][i]["item"]
        product_name = detected_item["name"]
        product_id = detected_item["id"]
        product_children = detected_item["children"]
        product = {
            "css_id": product_id,
            "name": product_name,
            "children": product_children
        }

        # fetching ingredient and nutrition values, if available
        product_metadata = {
            "ingredients": [],
            "amount": -1,
            "nutrition": {},
        }
        if(detected_item["nutrition_available"]):
            child_most_id = get_most_child_id(detected_item)
            product_metadata = get_nutrition_by_id(product_id=child_most_id)
        # obtaining nutrition from children, otherwise
        elif(not detected_item["nutrition_available"] and len(product_children) > 0):
            for child in product_children:
                if(child["nutrition_available"]):
                    children_id = child["id"]
                    product_metadata = get_nutrition_by_id(product_id=children_id)
                    print(product_metadata)
                    break

        # joining product metadata with high-level daa
        product = {**product, **product_metadata}
        products.append(product)

    with open("test.json", "w") as f:
        json.dump(products, f)

    return products


def get_nutrition_by_id(product_id):
    """
    Getting the nutrition value of a product given the product id

    Returns:
    --------
    metadata: {
        ingredients: [ingredient_1, ingredient_2, ..., ingredient_N],
        amount: 100 (grams),
        nutrition: {
            calories: 100,
            total_fat: 5,
            ...
        }
    }
    """

    api_key = Config.FOOD_RECOGNITION_KEY
    get_product_data_url = f"https://api-beta.bite.ai/items/{product_id}/"
    headers = {'Content-Type': 'application/json',
                'Authorization': 'Bearer {0}'.format(api_key)}

    response = requests.get(get_product_data_url, headers=headers)
    response = response.json()

    # fetching the metadata: product ingredients, nutrition values and amouts
    amount = -1
    nutrition = {}
    ingredients = response["text_ingredients"]
    nutrition_facts = response["nutrition_facts"]
    for fact in nutrition_facts:
        # enforcing using metric measurements
        if(fact["serving"]["unit"]["singular_name"] not in ["gram"]):
            continue
        amount = fact["serving"]["grams"]
        nutrition = fact["nutrition"]
    metadata = {
        "ingredients": ingredients,
        "amount": amount,
        "nutrition": nutrition
    }

    return metadata


def get_most_child_id(item):
    """
    Recursively navigating the children of the detected item to get id of the
    child-most item
    """

    id = item["id"]
    if("children" not in item.keys()):
        return id
    children = item["children"]
    if(len(children) > 0):
        id = get_most_child_id(children[0])
    return id

#
