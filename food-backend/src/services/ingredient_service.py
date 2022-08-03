from sqlalchemy.exc import IntegrityError
from flask import Blueprint, jsonify, request, make_response

from src.entities.entity import Session
from src.entities.ingredient import Ingredient, IngredientSchema

ingredient_blueprint = Blueprint("ingredient_blueprint", __name__)


@ingredient_blueprint.route("/ingredients")
def get_ingredients():
    # fetching ingredients from the database
    session = Session()
    ingredient_objects = session.query(Ingredient).all()

    # transforming ingredients into JSON-serializable objects
    schema = IngredientSchema(many=True)
    ingredients = schema.dump(ingredient_objects)

    session.close()
    # serializing as JSON
    return jsonify(ingredients), 200


@ingredient_blueprint.route("/ingredients", methods=["POST"])
def add_ingredient():
    try:
        posted_ingredient = IngredientSchema(only=("name", "rating")).load(
            request.get_json()
        )

        ingredient = Ingredient(**posted_ingredient)
        if ingredient.rating > 10 or ingredient.rating < 0:
            raise ValueError

        session = Session()
        session.add(ingredient)
        session.commit()

        new_ingredient = IngredientSchema().dump(ingredient)
        session.close()
        return jsonify(new_ingredient), 201
    except ValueError:
        error_message = "Rating must fall in range [0, 10]."
    except IntegrityError:
        error_message = "Ingredient name already exists."
    except Exception:
        error_message = "Something went wrong."
    return make_response(error_message, 400)
