from flask import Blueprint, jsonify, request, make_response

from src.entities.entity import Session
from src.entities.food_item import FoodItem, FoodItemSchema
from src.relations.food_item_extension import FoodItemExtension
from src.utils.food_item_utils import handle_food_item_crud, check_food_item_values, get_posted_food_item
from src.utils.utils import update_attribute, check_required, get_all, get_by_id

food_item_blueprint = Blueprint("food_item_blueprint", __name__)


@food_item_blueprint.route("/food-items")
@handle_food_item_crud
def get_food_items():
    food_items = get_all(FoodItem, FoodItemSchema)
    # Serializing as JSON
    return jsonify(food_items), 200

@food_item_blueprint.route("/food-items/<int:food_item_id>")
@handle_food_item_crud
def get_food_item(food_item_id):
    food_item = get_by_id(FoodItem, FoodItemSchema, food_item_id)
    # Serializing as JSON
    return jsonify(food_item), 200

@food_item_blueprint.route("/food-items", methods=["POST"])
@handle_food_item_crud
def add_food_item():
    posted_food_item = get_posted_food_item(request)

    check_required(posted_item=posted_food_item, required_attributes=["name"])

    check_food_item_values(posted_food_item)

    session = Session()
    food_item = FoodItem(**posted_food_item)
    session.add(food_item)
    session.commit()

    # Return created food item
    new_food_item = FoodItemSchema().dump(food_item)
    session.close()
    return jsonify(new_food_item), 201

@food_item_blueprint.route("/food-items/<int:food_item_id>", methods=["PUT"])
@handle_food_item_crud
def put_food_item(food_item_id):
    posted_food_item = get_posted_food_item(request)
    session = Session()
    food_item_object = (
        session.query(FoodItem).filter(FoodItem.id == food_item_id).one()
    )

    check_food_item_values(posted_food_item, update_mode=True, original_food_item=food_item_object)

    for attr in ["name", "is_wfd", "is_full_meal", "is_health_rotation", "season", "food_category_id"]:
        update_attribute(food_item_object, attribute=attr, new_value_dict=posted_food_item)
    session.commit()

    # Return edited food_item
    food_item = FoodItemSchema().dump(food_item_object)
    session.close()
    return jsonify(food_item), 200


@food_item_blueprint.route("/food-items/<int:food_item_id>", methods=["DELETE"])
@handle_food_item_crud
def delete_food_item(food_item_id):
    session = Session()
    food_item_object = (
        session.query(FoodItem).filter(FoodItem.id == food_item_id).one()
    )
    session.delete(food_item_object)
    session.commit()
    session.close()
    return make_response("Food item has been deleted.", 200)
