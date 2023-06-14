from marshmallow import Schema, fields
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from src.entities.entity import Base, Entity


class RecipeStatus(Entity, Base):
    __tablename__ = "recipe_statuses"

    name = Column(String, unique=True)

    def __init__(self, name):
        Entity.__init__(self)
        self.name = name


class RecipeStatusSchema(Schema):
    id = fields.Number()
    name = fields.Str()
