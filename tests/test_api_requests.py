"""
Testing the functionality of the API Requests processing libraries
"""

import os
import sys
from PIL import Image
import base64

sys.path.append("..")
import app.processing.api_requests as api_requests


def test_get_food_name():
    """
    Testing that the results of the Bite Food Recognition System works fine
    """

    img_path = os.path.join(os.getcwd(), "resources", "pizza.jpg")
    img = Image.open(img_path)
    # with open(img_path, "rb") as img:
        # img_base64 = base64.b64encode(img.read())
    # img = open(img_path, "rb")

    products = api_requests.get_food_name(img)
    print(products)

    return


def test_get_product_params():
    """
    """

    response = api_requests.get_product_by_name("salad", n_items=1)
    print(response)

    return


if __name__ == "__main__":
    os.system("clear")
    test_get_food_name()
    # test_get_product_params()

#