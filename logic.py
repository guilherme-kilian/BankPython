import datetime as dt
from app import db
from datetime import datetime
from domain.bankAccount import BankAccount
from domain.bankAccountType import BankAccountType
from domain.movement import Movement
from domain.movementType import MovementType
from domain.customer import Customer

class Logic():
    def __init__(self):
        super().__init__()
        
        self.session = db.session
    
    def init(self):        
        db.create_all()
        
        movementType = db.session.query(MovementType).all()
        bankAccountTypes = db.session.query(BankAccountType).all()
        
        if(len(movementType) == 0 and len(bankAccountTypes) == 0):
            self.add_initial_values()
        
        db.session.commit()
    
    def add_initial_values(self):
        movementTypes = [ MovementType(type='deposit'), MovementType(type='withdraw'), MovementType(type='fee')]
        bankAccountTypes = [ BankAccountType(type='current'), BankAccountType(type='savings'), BankAccountType(type='investiment')]
        db.session.add_all(movementTypes)
        db.session.add_all(bankAccountTypes)
    
    def create_user(self, name, document, gender, birthday):
        
        if(len(document) < 11):
            raise Exception("Invalid_Document")
                
        customer = self.get_customer_by_document(document)
        
        if(customer):
            raise Exception("Duplicated_Document")
        
        newCustomer = Customer(name=name, document=document, gender=gender, birthDay=datetime.strptime(birthday, '%Y-%m-%d'))
        self.session.add(newCustomer)
        self.session.commit()
        
        return newCustomer
        
    def open_account(self, document, accountType, initialBalance):
        customer = self.get_customer_by_document_or_error(document)
        
        if(customer.bankAccount):
            raise Exception("BankAccount_Already_Exists")
        
        bankAccountType = self.session.query(BankAccountType).where(BankAccountType.type == accountType).first()        
        
        if(bankAccountType == None):
            raise Exception("BankAccountType_NotFound")
        
        bankAccount = BankAccount(initial_balance=initialBalance, balance=initialBalance, bank_account_type=bankAccountType, customer=customer)
        self.add_and_save(bankAccount)
        
        return bankAccount
        
    def deposit(self, document, value):
        
        if(value < 0):
            raise Exception("Negative_Value")
        
        bankAccount = self.get_bankaccount_by_document_or_error(document)        
        bankAccount.balance += value        
        movement = self.add_movement(bankAccount, value, "deposit")        
        self.add_and_save(movement)
        return bankAccount
            
    def withdraw(self, document, value):
        bankAccount = self.get_bankaccount_by_document_or_error(document)
        
        if(value < 0):
            raise Exception("Negative_Value")
        
        if(bankAccount.balance < value):
            raise Exception('Insuficient_Balance')
        
        if(bankAccount.bank_account_type.type == "investiment"):
            raise Exception('Invalid_Account')
        
        bankAccount.balance -= value        
        movement = self.add_movement(bankAccount=bankAccount, value=value, type="withdraw")
        self.add_and_save(movement)
        
        return bankAccount
            
    def apply_fee(self, document, value):
        
        if(value < 0):
            raise Exception("Negative_Value")
        
        bankAccount = self.get_bankaccount_by_document_or_error(document)
        
        if(bankAccount.bank_account_type.type == "current"):
            raise Exception("Invalid_Account")
        
        bankAccount.balance += bankAccount.balance * (value / 100)
        movement = self.add_movement(bankAccount=bankAccount, value=value, type="fee")
        self.add_and_save(movement)
        
        return bankAccount
            
    def get_bank_statement(self, document, start, end):
        return  self.session.query(Movement).join(BankAccount).join(Customer).where(Customer.document == document).where(Movement.date > start).where(Movement.date < end).all()     
            
    def get_bankAccount_movement_by_document(self, document):
        return self.session.query(Movement).join(BankAccount).join(Customer).where(Customer.document == document).all()
            
    def add_movement(self, bankAccount, value, type):
        movementType = self.session.query(MovementType).where(MovementType.type == type).first()
        return Movement(date=dt.datetime.now(), value=value, movement_type=movementType, bank_account=bankAccount)
    
    def add_and_save(self, data):
        self.session.add(data)
        self.session.commit()
    
    def get_bankaccount_by_document_or_error(self, document):
        bankAccount = self.session.query(BankAccount).join(Customer).where(Customer.document == document).first()
        
        if(bankAccount is None):
            raise Exception("BankAccount_NotFound")
        
        return bankAccount
    
    def get_customer_by_document_or_error(self, document):
        
        customer = self.get_customer_by_document(document)
        
        if(customer is None):
            raise Exception("Customer_NotFound")
        
        return customer
    
    def get_customer_by_document(self, document):
        return self.session.query(Customer).where(Customer.document == document).first()
        