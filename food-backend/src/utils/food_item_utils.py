from functools import wraps

from flask import make_response
from marshmallow.exceptions import ValidationError
from sqlalchemy.exc import IntegrityError, NoResultFound

from src.entities.food_category import FoodCategory
from src.entities.food_item import FoodItem, FoodItemSchema
from src.utils.utils import check_existence, check_duplicate, check_range


def handle_food_item_crud(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except AttributeError:
            error_message = "Name is required."
        except ValidationError:
            error_message = "Attributes do not have the right datatype."
        except ValueError:
            error_message = "Season is not in range [0, 4095]."
        except NoResultFound:
            error_message = "Food item does not exist."
        except (NameError, IntegrityError):
            error_message = "Food item name already exists."
        except KeyError:
            error_message = "Food category does not exist."
        except Exception as e:
            error_message = "Something went wrong."
            print(type(e), e)
        return make_response(error_message, 400)
    return decorated


def get_months_from_season(season):
    months = []
    for i in range(12):
        if (1 << i) & season != 0:
            months.append(i)
    return months

def get_posted_food_item(request):
    posted_food_item = FoodItemSchema(only=("name",
                                            "is_wfd",
                                            "is_full_meal",
                                            "is_health_rotation",
                                            "season",
                                            "food_category_id")).load(request.get_json())
    return posted_food_item

def check_food_item_values(posted_food_item, update_mode=False, original_food_item=None):
    if "season" in posted_food_item:
        check_range(posted_food_item["season"], upper_bound=(1 << 12) - 1, lower_bound=0)

    if "name" in posted_food_item:
        if update_mode:
            if original_food_item.name != posted_food_item["name"]:
                check_duplicate(entity=FoodItem, attribute="name", value=posted_food_item["name"])
        else:
            check_duplicate(entity=FoodItem, attribute="name", value=posted_food_item["name"])

    if posted_food_item.get("food_category_id") is not None:
        check_existence(entity=FoodCategory, attribute="id", value=posted_food_item["food_category_id"])





