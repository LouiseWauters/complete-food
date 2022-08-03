from flask import Flask
from flask_cors import CORS

from src.entities.entity import engine, Base
from src.services.ingredient_service import ingredient_blueprint

# creating the Flask application
app = Flask(__name__)
CORS(app)

# generate database schema
Base.metadata.create_all(engine)

# Add ingredient blueprint to flask app
app.register_blueprint(ingredient_blueprint)
