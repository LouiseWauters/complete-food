from flask import Blueprint, jsonify

ingredient_blueprint = Blueprint("ingredient_blueprint", __name__)


# Test
@ingredient_blueprint.route("/ping")
def ping():
    return jsonify({"ping": "poooong"}), 200
