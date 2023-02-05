from functools import wraps

from flask import make_response
from sqlalchemy.exc import IntegrityError, NoResultFound


def check_rating_range(rating):
    if 10 < rating or rating < 0:
        raise ValueError


def handle_ingredient_crud(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except ValueError:
            error_message = "Rating must fall in range [0, 10]."
        except NoResultFound:
            error_message = "Ingredient does not exist."
        except (NameError, IntegrityError):
            error_message = "Ingredient name already exists."
        except KeyError:
            error_message = "Base ingredient does not exist."
        except Exception:
            error_message = "Something went wrong."
        return make_response(error_message, 400)

    return decorated
