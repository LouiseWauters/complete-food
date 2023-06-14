from flask import Blueprint, jsonify, request, make_response

from src.entities.entity import Session
from src.entities.recipe import Recipe, RecipeSchema
from src.utils.recipe_utils import handle_recipe_crud, get_posted_recipe, check_recipe_values
from src.utils.utils import update_attribute, check_required, get_all, get_by_id

recipe_blueprint = Blueprint("recipe_blueprint", __name__)


@recipe_blueprint.route("/recipes")
@handle_recipe_crud
def get_recipes():
    recipes = get_all(Recipe, RecipeSchema)
    # Serializing as JSON
    return jsonify(recipes), 200

@recipe_blueprint.route("/recipes/<int:recipe_id>")
@handle_recipe_crud
def get_recipe(recipe_id):
    recipe = get_by_id(Recipe, RecipeSchema, recipe_id)
    # Serializing as JSON
    return jsonify(recipe), 200

@recipe_blueprint.route("/recipes", methods=["POST"])
@handle_recipe_crud
def add_recipe():
    posted_recipe = get_posted_recipe(request)

    check_required(posted_item=posted_recipe, required_attributes=["food_item_id", "portions", "meal_time_category_id",
                                                                   "recipe_status_id"])
    check_recipe_values(posted_recipe)

    session = Session()
    recipe = Recipe(**posted_recipe)
    session.add(recipe)
    session.commit()

    # Return created Recipe
    new_recipe = RecipeSchema().dump(recipe)
    session.close()
    return jsonify(new_recipe), 201

@recipe_blueprint.route("/recipes/<int:recipe_id>", methods=["PUT"])
@handle_recipe_crud
def put_recipe(recipe_id):
    posted_recipe = get_posted_recipe(request)

    session = Session()
    recipe_object = (
        session.query(Recipe).filter(Recipe.id == recipe_id).one()
    )

    check_recipe_values(posted_recipe)

    for attr in ["food_item_id", "portions", "meal_time_category_id", "recipe_status_id", "original_source",
                 "cooking_time_min", "prep_time_min", "rest_time_min", "description", "estimated_price",
                 "alternative_title"]:
        update_attribute(recipe_object, attribute=attr, new_value_dict=posted_recipe)
    session.commit()

    # Return edited recipe
    recipe = RecipeSchema().dump(recipe_object)
    session.close()
    return jsonify(recipe), 200


@recipe_blueprint.route("/recipes/<int:recipe_id>", methods=["DELETE"])
@handle_recipe_crud
def delete_recipe(recipe_id):
    session = Session()
    recipe_object = (
        session.query(Recipe).filter(Recipe.id == recipe_id).one()
    )
    session.delete(recipe_object)
    session.commit()
    session.close()
    return make_response("Recipe has been deleted.", 200)
