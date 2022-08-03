from flask import Blueprint, jsonify

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
