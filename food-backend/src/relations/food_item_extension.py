from marshmallow import Schema, fields
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from src.entities.entity import Base


class FoodItemExtension(Base):
    __tablename__ = "food_item_extensions"

    base_food_id = Column(Integer, ForeignKey('food_items.id'), primary_key=True)
    extension_food_id = Column(Integer, ForeignKey('food_items.id'), primary_key=True)
    base_food_item = relationship("FoodItem", foreign_keys=[base_food_id], back_populates="extension_food_items")
    extension_food_item = relationship("FoodItem", foreign_keys=[extension_food_id], back_populates="base_food_items")


    def __init__(self, base_food_id, extension_food_id):
        super().__init__()
        self.base_food_id = base_food_id
        self.extension_food_id = extension_food_id


class FoodItemExtensionSchema(Schema):
    base_food_id = fields.Integer()
    extension_food_id = fields.Integer()

