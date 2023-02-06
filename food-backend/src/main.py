from flask import Flask
from flask_cors import CORS

from src.entities.entity import engine, Base
from src.services.ingredient_service import ingredient_blueprint
from src.services.food_item_service import food_item_blueprint

# creating the Flask application
app = Flask(__name__)
CORS(app)

# generate database schema
Base.metadata.create_all(engine)

# Add ingredient blueprint to flask app
app.register_blueprint(ingredient_blueprint)
app.register_blueprint(food_item_blueprint)
