from marshmallow import Schema, fields
from sqlalchemy import Column, String, Date, Integer, ForeignKey, Boolean, SmallInteger
from sqlalchemy.orm import relationship

from src.entities.entity import Base, Entity
from src.entities.food_category import FoodCategorySchema
from src.relations.food_item_extension import FoodItemExtensionSchema


class FoodItem(Entity, Base):
    __tablename__ = "food_items"
    name = Column(String, unique=True)
    last_eaten = Column(Date, nullable=True)
    times_eaten = Column(Integer, nullable=False)
    is_full_meal = Column(Boolean, nullable=False)
    is_wfd = Column(Boolean, nullable=False)
    is_health_rotation = Column(Boolean, nullable=False)
    season = Column(SmallInteger, nullable=False)
    food_category_id = Column(Integer, ForeignKey('food_categories.id'), nullable=True)
    recipe_link = Column(String, nullable=True)
    food_category = relationship("FoodCategory", backref="food_items")
    base_food_items = relationship("FoodItemExtension", back_populates="extension_food_item", primaryjoin='FoodItem.id==FoodItemExtension.extension_food_id')
    extension_food_items = relationship("FoodItemExtension", back_populates="base_food_item", primaryjoin='FoodItem.id==FoodItemExtension.base_food_id')

    def __init__(self, name, is_full_meal=False, is_wfd=False, is_health_rotation=False, season=4095,
                 food_category_id=None, recipe_link=None):
        Entity.__init__(self)
        self.name = name
        self.is_wfd = is_wfd
        self.is_full_meal = is_full_meal
        self.is_health_rotation = is_health_rotation
        self.season = season
        self.times_eaten = 0
        self.food_category_id = food_category_id
        self.recipe_link = recipe_link


class FoodItemSchema(Schema):
    id = fields.Integer()
    name = fields.Str()
    last_eaten = fields.Date()
    times_eaten = fields.Integer()
    is_full_meal = fields.Boolean()
    is_wfd = fields.Boolean()
    is_health_rotation = fields.Boolean()
    season = fields.Integer()
    food_category_id = fields.Integer(allow_none=True)
    recipe_link = fields.Str()
    food_category = fields.Pluck(FoodCategorySchema, 'name')
    base_food_items = fields.Pluck(FoodItemExtensionSchema, 'base_food_id', many=True)
    extension_food_items = fields.Pluck(FoodItemExtensionSchema, 'extension_food_id', many=True)
