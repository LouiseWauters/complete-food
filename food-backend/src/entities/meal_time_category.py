from marshmallow import Schema, fields
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from src.entities.entity import Base, Entity


class MealTimeCategory(Entity, Base):
    __tablename__ = "meal_time_categories"

    name = Column(String, unique=True)

    def __init__(self, name):
        Entity.__init__(self)
        self.name = name


class MealTimeCategorySchema(Schema):
    id = fields.Number()
    name = fields.Str()
