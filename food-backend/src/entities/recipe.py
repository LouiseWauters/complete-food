from marshmallow import Schema, fields
from sqlalchemy import Column, String, Integer, ForeignKey, Numeric
from sqlalchemy.orm import relationship

from src.entities.entity import Base, Entity
from src.entities.food_item import FoodItemSchema
from src.entities.meal_time_category import MealTimeCategorySchema
from src.entities.recipe_status import RecipeStatusSchema


class Recipe(Entity, Base):
    __tablename__ = "recipes"
    food_item_id = Column(Integer, ForeignKey('food_items.id'), nullable=False)
    portions = Column(Numeric, nullable=False)
    times_used = Column(Integer, nullable=False)
    meal_time_category_id = Column(Integer, ForeignKey('meal_time_categories.id'), nullable=False)
    recipe_status_id = Column(Integer, ForeignKey('recipe_statuses.id'), nullable=False)
    original_source = Column(String, nullable=True)
    cooking_time_min = Column(Integer, nullable=True)
    prep_time_min = Column(Integer, nullable=True)
    rest_time_min = Column(Integer, nullable=True)
    description = Column(String, nullable=True)
    estimated_price = Column(Numeric, nullable=True)
    alternative_title = Column(String, nullable=True)
    # image ??
    food_item = relationship('FoodItem', backref="recipes")
    meal_time_category = relationship("MealTimeCategory", backref="recipes")
    recipe_status = relationship("RecipeStatus", backref="recipes")

    def __init__(self, food_item_id, portions, meal_time_category_id, recipe_status_id, original_source=None,
                 cooking_time_min=None, prep_time_min=None, rest_time_min=None, description=None, estimated_price=None,
                 alternative_title=None):
        Entity.__init__(self)
        self.food_item_id = food_item_id
        self.portions = portions
        self.times_used = 0
        self.meal_time_category_id = meal_time_category_id
        self.recipe_status_id = recipe_status_id
        self.original_source = original_source
        self.cooking_time_min = cooking_time_min
        self.prep_time_min = prep_time_min
        self.rest_time_min = rest_time_min
        self.description = description
        self.estimated_price = estimated_price
        self.alternative_title = alternative_title


class RecipeSchema(Schema):
    id = fields.Integer()
    food_item_id = fields.Integer()
    portions = fields.Number()
    times_used = fields.Integer()
    meal_time_category_id = fields.Integer()
    recipe_status_id = fields.Integer()
    original_source = fields.Str()
    cooking_time_min = fields.Integer()
    prep_time_min = fields.Integer()
    rest_time_min = fields.Integer()
    description = fields.Str()
    estimated_price = fields.Number()
    alternative_title = fields.Str()
    food_item = fields.Nested(FoodItemSchema)
    meal_time_category = fields.Pluck(MealTimeCategorySchema, 'name')
    recipe_status = fields.Pluck(RecipeStatusSchema, 'name')





