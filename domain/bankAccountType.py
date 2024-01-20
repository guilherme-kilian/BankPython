from sqlalchemy import Column, Integer, String
from app import db

class BankAccountType(db.Model):
    __tablename__ = 'bankAccountType'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    type = Column(String(255))