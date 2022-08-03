from sqlalchemy import Column, String, Float, Date

from src.entities.entity import Base, Entity


class Ingredient(Entity, Base):
    __tablename__ = "ingredienten"

    name = Column(String, unique=True)
    rating = Column(Float)
    last_eaten = Column(Date)

    def __init__(self, name, rating):
        Entity.__init__(self)
        self.name = name
        self.rating = rating
