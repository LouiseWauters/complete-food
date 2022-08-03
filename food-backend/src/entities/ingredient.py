from marshmallow import Schema, fields
from sqlalchemy import Column, String, Float, Date

from src.entities.entity import Base, Entity


class Ingredient(Entity, Base):
    __tablename__ = "ingredients"

    name = Column(String, unique=True)
    rating = Column(Float)
    last_eaten = Column(Date)

    def __init__(self, name, rating):
        Entity.__init__(self)
        self.name = name
        self.rating = rating


class IngredientSchema(Schema):
    id = fields.Number()
    name = fields.Str()
    rating = fields.Float()
    last_eaten = fields.Date()
