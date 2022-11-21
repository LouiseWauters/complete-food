from marshmallow import Schema, fields
from sqlalchemy import Column, String, Float, Date, Integer, ForeignKey, Boolean

from src.entities.entity import Base, Entity


class Ingredient(Entity, Base):
    __tablename__ = "ingredients"

    name = Column(String, unique=True)
    rating = Column(Float)
    last_eaten = Column(Date)
    is_vegetable = Column(Boolean)
    base_ingredient_id = Column(Integer, ForeignKey('ingredients.id'), nullable=True)

    def __init__(self, name, rating, is_vegetable=False, base_ingredient_id=None):
        Entity.__init__(self)
        self.name = name
        self.rating = rating
        self.is_vegetable = is_vegetable
        if base_ingredient_id:
            self.base_ingredient_id = base_ingredient_id


class IngredientSchema(Schema):
    id = fields.Number()
    name = fields.Str()
    rating = fields.Float()
    last_eaten = fields.Date()
    is_vegetable = fields.Boolean()
    base_ingredient_id = fields.Number(allow_none=True)
