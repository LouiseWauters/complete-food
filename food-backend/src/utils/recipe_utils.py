import math
from functools import wraps

from flask import make_response

from src.entities.food_item import FoodItem
from src.entities.meal_time_category import MealTimeCategory
from src.entities.recipe import RecipeSchema
from src.entities.recipe_status import RecipeStatus
from src.utils.utils import check_existence, check_range


def handle_recipe_crud(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        # TODO catch specific exceptions and write relevant error messages
        except Exception as e:
            error_message = "Something went wrong."
            print(type(e), e)
        return make_response(error_message, 400)
    return decorated

def get_posted_recipe(request):
    posted_recipe = RecipeSchema(only=("food_item_id",
                                       "portions",
                                       "meal_time_category_id",
                                       "recipe_status_id",
                                       "original_source",
                                       "cooking_time_min",
                                       "prep_time_min",
                                       "rest_time_min",
                                       "description",
                                       "estimated_price",
                                       "alternative_title")).load(request.get_json())
    return posted_recipe

def check_recipe_values(posted_recipe):
    if "portions" in posted_recipe:
        check_range(posted_recipe["portions"], upper_bound=math.inf, lower_bound=0)

    if "cooking_time_min" in posted_recipe:
        check_range(posted_recipe["cooking_time_min"], upper_bound=math.inf, lower_bound=0)

    if "prep_time_min" in posted_recipe:
        check_range(posted_recipe["prep_time_min"], upper_bound=math.inf, lower_bound=0)

    if "rest_time_min" in posted_recipe:
        check_range(posted_recipe["rest_time_min"], upper_bound=math.inf, lower_bound=0)

    # TODO add update mode and original recipe, because existence should not be checked if the new ids are not
    #  different from the old ones

    if "food_item_id" in posted_recipe:
        check_existence(entity=FoodItem, attribute="id", value=posted_recipe["food_item_id"])

    if "meal_time_category_id" in posted_recipe:
        check_existence(entity=MealTimeCategory, attribute="id", value=posted_recipe["meal_time_category_id"])

    if "recipe_status_id" in posted_recipe:
        check_existence(entity=RecipeStatus, attribute="id", value=posted_recipe["recipe_status_id"])
