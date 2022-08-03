from flask import Blueprint, jsonify

from src.entities.entity import Session
from src.entities.ingredient import Ingredient

ingredient_blueprint = Blueprint("ingredient_blueprint", __name__)


@ingredient_blueprint.route("/ingredients")
def get_ingredients():
    # fetching ingredients from the database
    session = Session()
    ingredient_objects = session.query(Ingredient).all()

    # transforming ingredients into json objects
    ingredients = [ingredient.to_json() for ingredient in ingredient_objects]

    session.close()
    return jsonify(ingredients), 200
