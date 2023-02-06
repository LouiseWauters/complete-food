from functools import wraps

from flask import make_response
from sqlalchemy.exc import IntegrityError, NoResultFound


def handle_food_item_crud(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except NoResultFound:
            error_message = "Food item does not exist."
        except (NameError, IntegrityError):
            error_message = "Food item name already exists."
        except KeyError:
            error_message = "All attributes need to be included."
        except Exception:
            error_message = "Something went wrong."
        return make_response(error_message, 400)
    return decorated


def get_months_from_season(season):
    months = []
    for i in range(12):
        if (1 << i) & season != 0:
            months.append(i)
    return months
