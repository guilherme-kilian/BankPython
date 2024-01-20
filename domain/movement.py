from sqlalchemy import Column, Integer, Float, Date,ForeignKey
from app import db
import sqlalchemy.orm as orm
from domain.bankAccount import BankAccount
from domain.movementType import MovementType

class Movement(db.Model):
    __tablename__ = 'movement'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    date = Column(Date)
    value = Column(Float)
    movement_type_id = Column(Integer, ForeignKey(MovementType.id), nullable=False)
    movement_type = orm.relationship(MovementType)
    bank_account_id = Column(Integer, ForeignKey(BankAccount.id), nullable=False)
    bank_account = orm.relationship(BankAccount, backref='bankAccount', foreign_keys=[bank_account_id])   