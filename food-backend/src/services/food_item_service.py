from flask import Blueprint, jsonify, request, make_response

from src.entities.entity import Session
from src.entities.food_item import FoodItem, FoodItemSchema
from src.relations.food_item_extension import FoodItemExtension, FoodItemExtensionSchema
from src.utils.food_item_utils import handle_food_item_crud, check_food_item_values, get_posted_food_item, \
    get_all_base_food_items
from src.utils.utils import update_attribute, check_required, get_all, get_by_id, get_by_ids, check_existence
from src.utils.exceptions import CircularDependencyError
food_item_blueprint = Blueprint("food_item_blueprint", __name__)


@food_item_blueprint.route("/food-items")
@handle_food_item_crud
def get_food_items():
    food_items = get_all(FoodItem, FoodItemSchema)
    # Serializing as JSON
    return jsonify(food_items), 200


@food_item_blueprint.route("/food-items/<int:food_item_id>/all-bases")
@handle_food_item_crud
def get_all_food_item_bases(food_item_id):
    food_item = get_by_id(FoodItem, FoodItemSchema, food_item_id)
    base_item_ids = get_all_base_food_items(food_item)
    bases = get_by_ids(FoodItem, FoodItemSchema, base_item_ids)
    # Serializing as JSON
    return jsonify(bases), 200

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

    for attr in ["name", "is_wfd", "is_full_meal", "is_health_rotation", "season", "food_category_id", "recipe_link"]:
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

@food_item_blueprint.route("/food-items/<int:base_id>/extensions/<int:extension_id>", methods=["POST"])
@handle_food_item_crud
def add_food_item_extension(base_id, extension_id):

    base_food_item = get_by_id(entity=FoodItem, entity_schema=FoodItemSchema, item_id=base_id)
    all_base_ids = get_all_base_food_items(base_food_item)
    check_existence(entity=FoodItem, attribute="id", value=extension_id)

    if extension_id in all_base_ids or extension_id == base_id:
        raise CircularDependencyError

    session = Session()
    extension = FoodItemExtension(base_food_id=base_id, extension_food_id=extension_id)
    session.add(extension)
    session.commit()

    # Return created extension
    new_extension = FoodItemExtensionSchema().dump(extension)
    session.close()
    return jsonify(new_extension), 201


@food_item_blueprint.route("/food-items/<int:base_id>/extensions/<int:extension_id>", methods=["DELETE"])
@handle_food_item_crud
def delete_food_item_extension(base_id, extension_id):
    session = Session()
    food_item_extension_object = (
        session.query(FoodItemExtension)
        .filter(FoodItemExtension.base_food_id == base_id)
        .filter(FoodItemExtension.extension_food_id == extension_id)
        .one()
    )
    session.delete(food_item_extension_object)
    session.commit()
    session.close()
    return make_response("Food item extension has been deleted.", 200)
