from flask import Blueprint, jsonify, request, make_response

from src.entities.entity import Session
from src.entities.food_category import FoodCategory, FoodCategorySchema
from src.utils.food_category_utils import handle_food_category_crud
from src.utils.utils import update_attribute, check_duplicate, check_required

food_category_blueprint = Blueprint("food_category_blueprint", __name__)


@food_category_blueprint.route("/food-categories")
@handle_food_category_crud
def get_food_categories():
    # TODO refactor because this code can be reused
    # Fetching food categories from the database
    session = Session()
    food_category_objects = session.query(FoodCategory).all()

    # Transforming food categories into JSON-serializable objects
    schema = FoodCategorySchema(many=True)
    food_categories = schema.dump(food_category_objects)

    session.close()
    # Serializing as JSON
    return jsonify(food_categories), 200

@food_category_blueprint.route("/food-categories/<int:food_category_id>")
@handle_food_category_crud
def get_food_category(food_category_id):
    # TODO refactor because this code can be reused
    # Fetching food category from the database
    session = Session()
    food_category_object = session\
        .query(FoodCategory)\
        .filter(FoodCategory.id == food_category_id)\
        .one()

    # Transforming food categories into JSON-serializable objects
    schema = FoodCategorySchema(many=False)
    food_category = schema.dump(food_category_object)

    session.close()
    # Serializing as JSON
    return jsonify(food_category), 200

@food_category_blueprint.route("/food-categories", methods=["POST"])
@handle_food_category_crud
def add_food_category():
    posted_food_category = FoodCategorySchema(only=("name",)).load(request.get_json())

    check_required(posted_item=posted_food_category, required_attributes=["name"])
    check_duplicate(entity=FoodCategory, attribute="name", value=posted_food_category["name"])

    session = Session()
    food_category = FoodCategory(**posted_food_category)
    session.add(food_category)
    session.commit()

    # Return created food category
    new_food_category = FoodCategorySchema().dump(food_category)
    session.close()
    return jsonify(new_food_category), 201

@food_category_blueprint.route("/food-categories/<int:food_category_id>", methods=["PUT"])
@handle_food_category_crud
def put_food_category(food_category_id):
    posted_food_category = FoodCategorySchema(only=("name",)).load(request.get_json())
    session = Session()
    food_category_object = (
        session.query(FoodCategory).filter(FoodCategory.id == food_category_id).one()
    )
    if posted_food_category.get("name") is not None:
        if food_category_object.name != posted_food_category["name"]:
            check_duplicate(entity=FoodCategory, attribute="name", value=posted_food_category["name"])
            update_attribute(food_category_object, attribute="name", new_value_dict=posted_food_category)
    session.commit()

    # Return edited food_category
    food_category = FoodCategorySchema().dump(food_category_object)
    session.close()
    return jsonify(food_category), 200


@food_category_blueprint.route("/food-categories/<int:food_category_id>", methods=["DELETE"])
@handle_food_category_crud
def delete_food_category(food_category_id):
    session = Session()
    food_category_object = (
        session.query(FoodCategory).filter(FoodCategory.id == food_category_id).one()
    )
    session.delete(food_category_object)
    session.commit()
    session.close()
    return make_response("Food category has been deleted.", 200)
