from marshmallow import Schema, fields
from sqlalchemy import Column, String, Date, Integer, ForeignKey, Boolean, SmallInteger
from sqlalchemy.orm import relationship

from src.entities.entity import Base, Entity
from src.entities.food_category import FoodCategorySchema


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
    food_category = relationship("FoodCategory", backref="food_items")

    def __init__(self, name, is_full_meal=False, is_wfd=False, is_health_rotation=False, season=4095,
                 food_category_id=None):
        Entity.__init__(self)
        self.name = name
        self.is_wfd = is_wfd
        self.is_full_meal = is_full_meal
        self.is_health_rotation = is_health_rotation
        self.season = season
        self.times_eaten = 0
        self.food_category_id = food_category_id


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
    food_category = fields.Pluck(FoodCategorySchema, 'name')