from sqlalchemy import Column, Integer, String
from app import db

class MovementType(db.Model):
    __tablename__ = 'movementType'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    type = Column(String(255))