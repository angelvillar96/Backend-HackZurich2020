"""
Handling requests to Migros and Bite APIs for fetching data
"""

import json
import requests

from config import Config


def get_food_name(img):
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
    # print(data)

    response = requests.post(food_recognition_url, json=data, headers=headers)
    response = response.json()

    return response

#


def get_product_by_name(product_name, n_items=5):
    """
    Getting the nutrition and product parameters given product_name
    """

    api_key = Config.FOOD_RECOGNITION_KEY
    get_product_url = "https://api-beta.bite.ai/products/search"
    headers = {'Content-Type': 'application/json',
                'Authorization': 'Bearer {0}'.format(api_key)}

    params = {
        "query": product_name
    }
    response = requests.get(get_product_url, params=params, headers=headers)
    response = response.json()

    counts = response["count"]
    products = response["results"]
    products = [p for p in products[:n_items]]

    for product in products:
        p = {}
        p_id = product["id"]
        p_name = product["name"]
        if(product["nutrition_available"]):
            get_nutrition_by_id(p_id)

    return products


def get_nutrition_by_id(id):
    """
    Getting the nutrition value of a product given the product id
    """

    api_key = Config.FOOD_RECOGNITION_KEY
    get_product_url = "https://api-beta.bite.ai/products/search"
    headers = {'Content-Type': 'application/json',
                'Authorization': 'Bearer {0}'.format(api_key)}

    params = {
        "query": product_name
    }
    response = requests.get(get_product_url, params=params, headers=headers)
    response = response.json()


    return
