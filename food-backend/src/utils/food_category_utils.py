from functools import wraps

from flask import make_response
from sqlalchemy.exc import NoResultFound


def handle_food_category_crud(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except AttributeError as e:
            error_message = e.args[0]
        except NameError:
            error_message = "Name already exists."
        except NoResultFound:
            error_message = "Food category does not exist."
        except Exception as e:
            error_message = "Something went wrong."
            print(type(e), e)
        return make_response(error_message, 400)
    return decorated
