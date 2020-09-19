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
    img: image in format base 64

    Returns:
    --------
    products = [
        {
            css_id: 12121-15161-32165161,
            name: cheese,
            children: [{},{}]
            ingredients: [ing1, ing2, ...],
            amount:
            nutrition: {
                calories: 100,
                sugar: 20,
                ...
            }
        }
    ]
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


def get_product_by_name(product_name):
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

    product = response["results"][0]

    return product


def get_recipes_by_ingredient(ingredient, n_items=5):
    """
    Obtaining a bunch of recipes given an ingredient
    """

    ingredient_name = ingredient["name"]
    ingredient_name = "Reis"

    auth = Config.MIGROS_AUTH
    get_recipe_url = "https://hackzurich-api.migros.ch/hack/recipe/recipes_de/_search"
    headers = {'Content-Type': 'application/json'}

    params = {"query": {"nested":{"path":"ingredients",
                                "query": {"term": {"ingredients.name.singular":ingredient_name}}}}}

    response = requests.post(get_recipe_url, json=params, auth=auth, headers=headers)
    response = response.json()

    returned_recipes = response["hits"]["hits"]
    recipes = []
    for cur_recipe in returned_recipes:

        # api recipe identifiers
        recipe_id = cur_recipe["_id"]
        recipe_score = cur_recipe["_score"]

        # general recipe information for the user
        recipe_title = cur_recipe["_source"]["title"]
        recipe_teaser = cur_recipe["_source"]["teasertext"]
        recipe_nutrients = cur_recipe["_source"]["nutrients"]
        _images_data = cur_recipe["_source"]["images"]
        recipe_image_url = _images_data[0]["ratios"][0]["stack"].replace("{stack}", "medium")

        # dont really know what this is
        taxonomy_data = cur_recipe["_source"]["taxonomies"]
        taxonomies = [t["name"] for t in taxonomy_data]

        # cooking procedure : ingredients and instructions
        cooking_time = cur_recipe["_source"]["duration_total_in_minutes"]
        instructions = cur_recipe["_source"]["steps"][0]["description"]
        _ingredients_data = cur_recipe["_source"]["ingredients"]
        _ingredients = [i["name"]["singular"] for i in _ingredients_data]
        _ingredients_size_data = cur_recipe["_source"]["sizes"]
        ingredients = {}
        ingredients["ingredients"] = _ingredients
        ingredients["sizes"] = {}
        for cur_size_data in _ingredients_size_data:
            # print(cur_size_data)
            number_eaters = cur_size_data["text"]
            cur_ingredients = cur_size_data["ingredient_blocks"][0]["ingredients"]
            cur_sizes = {c["text"]:c["amount"]["text"] for c in cur_ingredients}
            ingredients["sizes"][number_eaters] = cur_sizes

        # tags to display to the user
        _tags_data = cur_recipe["_source"]["tags"]
        contains_allergens = [t["name"] for t in _tags_data if t["type"] in ["contains"]]
        nutrition_type = [t["name"] for t in _tags_data if t["type"] in ["nutrition-philosophy"]]
        tags = [t["name"] for t in _tags_data if t["type"] in ["ocassions", "region",
                                                              "season","nutrition-philosophy",
                                                              "recipe-difficulty"]]
        recipe = {
            "id": recipe_id,
            "score": recipe_score,
            "general_info": {
                "title": recipe_title,
                "teaser": recipe_teaser,
                "nutrition": recipe_nutrients,
                "image_url": recipe_image_url
            },
            "cooking_instructions": {
                "time": cooking_time,
                "instructions": instructions,
                "ingredients": ingredients
            },
            "allergens": contains_allergens,
            "nutrition_type": nutrition_type,
            "tags": tags
        }
        recipes.append(recipe)

    with open("recipes.json", "w") as f:
        json.dump(recipes, f)

    return recipes


def css_to_migros_product(css_product):
    """
    Given a product from the css database, finding the equivalent from the
    migros database
    """

    product_name = css_product["name"]
    product_name = "Sofa"
    print(product_name)

    auth = Config.MIGROS_AUTH
    get_product_url = f"https://hackzurich-api.migros.ch/products"
    headers = {'Content-Type': 'application/json'}
    # params = {"q": "name: Feen"}
    params = {"query": {"nested":{"path":"products",
                                  "query": {"match": {"name.id":product_name}}}}}
    # params = {'query': {'match': {'name': product_name}}}

    # filters for retreving the product information
    response = requests.get(get_product_url, params=params, auth=auth, headers=headers)
    response = response.json()

    print("\n")
    print(response.keys())
    print("\n")
    print(len(response["products"]))
    print("\n")
    print(response["products"][0].keys())
    # print(response["products"][0]["name"])
    # names = [n["name"] for n in response["products"]]
    names = [n["slug"] for n in response["products"]]
    print(names)

    exit()

    return migros_product


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
