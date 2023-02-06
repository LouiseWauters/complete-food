from flask import Blueprint, jsonify, request, make_response

from src.entities.entity import Session
from src.entities.ingredient import Ingredient, IngredientSchema
from src.services.ingredient_utils import handle_ingredient_crud
from src.services.utils import check_range

ingredient_blueprint = Blueprint("ingredient_blueprint", __name__)


@ingredient_blueprint.route("/ingredients")
@handle_ingredient_crud
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
@handle_ingredient_crud
def add_ingredient():
    posted_ingredient = IngredientSchema(only=("name", "rating", "is_vegetable", "base_ingredient_id")).load(
        request.get_json()
    )

    check_range(posted_ingredient["rating"], upper_bound=10, lower_bound=0)

    session = Session()
    # Check if name already exists
    if (
        session.query(Ingredient)
        .filter(Ingredient.name == posted_ingredient["name"])
        .first()
        is not None
    ):
        raise NameError

    # Check if base ingredient id is valid
    if posted_ingredient["base_ingredient_id"]:
        if (
            session.query(Ingredient)
            .filter(Ingredient.id == posted_ingredient["base_ingredient_id"])
            .first()
            is None
        ):
            raise KeyError

    ingredient = Ingredient(**posted_ingredient)
    session.add(ingredient)
    session.commit()

    # Return created ingredient
    new_ingredient = IngredientSchema().dump(ingredient)
    session.close()
    return jsonify(new_ingredient), 201


@ingredient_blueprint.route("/ingredients/<int:ingredient_id>", methods=["PUT"])
@handle_ingredient_crud
def put_ingredient(ingredient_id):
    data = request.get_json()

    check_range(data["rating"], upper_bound=10, lower_bound=0)

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


@ingredient_blueprint.route("/ingredients/<int:ingredient_id>", methods=["DELETE"])
@handle_ingredient_crud
def delete_ingredient(ingredient_id):
    session = Session()
    ingredient_object = (
        session.query(Ingredient).filter(Ingredient.id == ingredient_id).one()
    )
    session.delete(ingredient_object)
    session.commit()
    session.close()
    return make_response("Ingredient has been deleted.", 200)
