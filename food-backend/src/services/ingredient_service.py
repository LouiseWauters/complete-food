from sqlalchemy.exc import IntegrityError, NoResultFound
from flask import Blueprint, jsonify, request, make_response

from src.entities.entity import Session
from src.entities.ingredient import Ingredient, IngredientSchema

ingredient_blueprint = Blueprint("ingredient_blueprint", __name__)


@ingredient_blueprint.route("/ingredients")
def get_ingredients():
    # Fetching ingredients from the database
    session = Session()
    ingredient_objects = session.query(Ingredient).all()

    # Transforming ingredients into JSON-serializable objects
    schema = IngredientSchema(many=True)
    ingredients = schema.dump(ingredient_objects)

    session.close()
    # Serializing as JSON
    return jsonify(ingredients), 200


@ingredient_blueprint.route("/ingredients", methods=["POST"])
def add_ingredient():
    try:
        posted_ingredient = IngredientSchema(only=("name", "rating")).load(
            request.get_json()
        )

        # Check rating range
        if 10 < posted_ingredient["rating"] or posted_ingredient["rating"] < 0:
            raise ValueError

        session = Session()
        # Check if name already exists
        if (
            session.query(Ingredient)
            .filter(Ingredient.name == posted_ingredient["name"])
            .first()
            is not None
        ):
            raise NameError

        ingredient = Ingredient(**posted_ingredient)
        session.add(ingredient)
        session.commit()

        # Return created ingredient
        new_ingredient = IngredientSchema().dump(ingredient)
        session.close()
        return jsonify(new_ingredient), 201
    except ValueError:
        error_message = "Rating must fall in range [0, 10]."
    except (NameError, IntegrityError):
        error_message = "Ingredient name already exists."
    except Exception:
        error_message = "Something went wrong."
    return make_response(error_message, 400)


@ingredient_blueprint.route("/ingredient/<int:ingredient_id>", methods=["PUT"])
def put_ingredient(ingredient_id):
    try:
        data = request.get_json()

        # Check rating range
        if 10 < data["rating"] or data["rating"] < 0:
            raise ValueError

        session = Session()
        ingredient_object = (
            session.query(Ingredient).filter(Ingredient.id == ingredient_id).one()
        )
        ingredient_object.name = data["name"]
        ingredient_object.rating = data["rating"]
        session.commit()

        # Return edited ingredient
        ingredient = IngredientSchema().dump(ingredient_object)
        session.close()
        return jsonify(ingredient), 200
    except ValueError:
        error_message = "Rating must fall in range [0, 10]."
    except IntegrityError:
        error_message = "Ingredient name already exists."
    except NoResultFound:
        error_message = "Ingredient does not exist."
    except Exception:
        error_message = "Something went wrong."
    return make_response(error_message, 400)


@ingredient_blueprint.route("/ingredient/<int:ingredient_id>", methods=["DELETE"])
def delete_ingredient(ingredient_id):
    try:
        session = Session()
        ingredient_object = (
            session.query(Ingredient).filter(Ingredient.id == ingredient_id).one()
        )
        session.delete(ingredient_object)
        session.commit()
        session.close()
        return make_response("Ingredient has been deleted.", 204)
    except NoResultFound:
        error_message = "Ingredient does not exist."
    except Exception:
        error_message = "Something went wrong."
    return make_response(error_message, 400)
