from flask import Blueprint, jsonify, request, make_response

from src.entities.entity import Session
from src.entities.food_item import FoodItem, FoodItemSchema
from src.utils.food_item_utils import handle_food_item_crud
from src.utils.utils import check_range

food_item_blueprint = Blueprint("food_item_blueprint", __name__)


@food_item_blueprint.route("/food-items")
@handle_food_item_crud
def get_food_items():
    # Fetching food items from the database
    session = Session()
    food_item_objects = session.query(FoodItem).all()

    # Transforming food items into JSON-serializable objects
    schema = FoodItemSchema(many=True)
    food_items = schema.dump(food_item_objects)

    session.close()
    # Serializing as JSON
    return jsonify(food_items), 200

@food_item_blueprint.route("/food-items/<int:food_item_id>")
@handle_food_item_crud
def get_food_item(food_item_id):
    # Fetching food item from the database
    session = Session()
    food_item_object = session\
        .query(FoodItem)\
        .filter(FoodItem.id == food_item_id)\
        .one()

    # Transforming food items into JSON-serializable objects
    schema = FoodItemSchema(many=False)
    food_item = schema.dump(food_item_object)

    session.close()
    # Serializing as JSON
    return jsonify(food_item), 200

@food_item_blueprint.route("/food-items", methods=["POST"])
@handle_food_item_crud
def add_food_item():
    posted_food_item = FoodItemSchema(only=("name",
                                            "is_wfd",
                                            "is_full_meal",
                                            "is_health_rotation",
                                            "season")).load(request.get_json())
    # TODO Check season with base food items (bitwise an
    if posted_food_item.get("season") is not None:
        check_range(posted_food_item["season"], upper_bound=(1 << 12) - 1, lower_bound=0)
    session = Session()
    # Check if name already exists
    if (
            session.query(FoodItem)
                    .filter(FoodItem.name == posted_food_item["name"])
                    .first()
            is not None
    ):
        raise NameError

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
    posted_food_item = FoodItemSchema(only=("name",
                                            "is_wfd",
                                            "is_full_meal",
                                            "is_health_rotation",
                                            "season")).load(request.get_json())
    check_range(posted_food_item["season"], upper_bound=(1 << 12) - 1, lower_bound=0)
    session = Session()
    food_item_object = (
        session.query(FoodItem).filter(FoodItem.id == food_item_id).one()
    )
    # Check if name already exists
    if food_item_object.name != posted_food_item["name"]:
        if (
                session.query(FoodItem)
                        .filter(FoodItem.name == posted_food_item["name"])
                        .first()
                is not None
        ):
            raise NameError
    food_item_object.name = posted_food_item["name"]
    food_item_object.is_wfd = posted_food_item["is_wfd"]
    food_item_object.is_full_meal = posted_food_item["is_full_meal"]
    food_item_object.is_health_rotation = posted_food_item["is_health_rotation"]
    food_item_object.season = posted_food_item["season"]
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
