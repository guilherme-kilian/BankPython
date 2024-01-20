from sqlalchemy import Column, Integer, Float, ForeignKey
from app import db
import sqlalchemy.orm as orm
from domain.bankAccountType import BankAccountType
from domain.customer import Customer

class BankAccount(db.Model):
    __tablename__ = 'bankAccount'
    __table_args__ = { 'extend_existing': True }
    id = Column(Integer, primary_key=True)
    initial_balance = Column(Float)
    balance = Column(Float)
    bank_account_type_id = Column(Integer, ForeignKey(BankAccountType.id), nullable=False)        
    bank_account_type = orm.relationship(BankAccountType)
    customer_id = Column(Integer, ForeignKey(Customer.id, ondelete="CASCADE"), nullable=False)
    customer = orm.relationship(Customer, backref='bankAccount', foreign_keys=[customer_id])