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

    def to_json(self):
        return {
            "name": self.name,
            "rating": self.rating,
            "id": self.id,
            "last_eaten": self.last_eaten,
        }
