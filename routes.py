from app import app
from flask import render_template, request, make_response
from logic import *
from model.movementModel import MovementModel
import json

logic = Logic()

@app.route('/')
@app.route('/index', methods=['GET'])
def index():
    logic.init()
    return render_template('index.html')

@app.route('/exit', methods=['GET'])
def exit():
    return render_template('exit.html')

@app.route('/customer', methods=['GET'])
def customer():
    return render_template('customer.html')

@app.route('/customer', methods=['POST'])
def customer_post():
    name = request.form['name']
    document = request.form['document']
    gender = request.form['gender']
    birthday = request.form['birthday']
    try:        
        newCustomer = logic.create_user(name, document, gender, birthday)
        return render_template('customer.html', newCustomer=newCustomer)
    except Exception as ex:
        errorMessage = 'Erro interno.'
        if(str(ex) == 'Invalid_Document'):
            errorMessage = "CPF inválido."        
        if str(ex) == 'Duplicated_Document':
            errorMessage = 'Já existe um usuário com esta conta.'
        return render_template('customer.html', error=errorMessage)

@app.route('/account', methods=['GET'])
def account():
    return render_template('account.html')

@app.route('/account', methods=['POST'])
def account_post():
    document = request.form['document']
    accountType = request.form['bankAccountType']
    initialBalance = float(request.form['initial_balance'])
    
    try:
        bankAccount = logic.open_account(document, accountType, initialBalance)
        return render_template('account.html', bankAccount=bankAccount)
    except Exception as ex:
        errorMessage = 'Erro interno.'
        if str(ex) == 'BankAccount_Already_Exists':
            errorMessage = 'Este usuário já possui uma conta bancária.'
        if(str(ex) == 'BankAccountType_NotFound'):
            errorMessage = 'Categoria da conta bancária não encontrada.'
                    
        return render_template('account.html', error=errorMessage)

@app.route('/bankinterest', methods=['GET'])
def bankinterest():
    return render_template('bankinterest.html')

@app.route('/bankinterest', methods=['POST'])
def bankinterest_post():    
    document = request.form['document']
    value = float(request.form['value'])
    
    try:
        bankAccount = logic.apply_fee(document, value)
        return render_template('bankinterest.html', bankAccount=bankAccount)
    except Exception as ex:
        errorMessage = 'Erro interno.'
        if str(ex) == 'Invalid_Account':
            errorMessage = 'Conta inválida'
        if str(ex) == 'BankAccount_NotFound':
            errorMessage = 'Conta bancária não encontrada.'
        if(str(ex) == 'Negative_Value'):
            errorMessage = 'Valor do juros precisa ser maior que zero.'
        
        return render_template('bankinterest.html', error=errorMessage)

@app.route('/withdraw', methods=['GET'])
def withdraw():
    return render_template('withdraw.html')

@app.route('/withdraw', methods=['POST'])
def withdraw_post():
    document = request.form['document']
    value = float(request.form['value'])
    try:
        bankAccount = logic.withdraw(document, value)
        return render_template('withdraw.html', bankAccount=bankAccount)
    except Exception as ex:
        errorMessage = 'Erro interno.'
        if str(ex) == 'BankAccount_NotFound':
            errorMessage = 'Conta bancária não encontrada.'
        if str(ex) == 'Invalid_Account':
            errorMessage = 'Esta conta não pode realizar saques.'
        if(str(ex) == 'Insuficient_Balance'):
            errorMessage = 'Saldo insuficiente para realizar o saque.'  
        if(str(ex) == 'Negative_Value'):
            errorMessage = 'Valor do saque precisa ser maior que zero.'
        return render_template('withdraw.html', error=errorMessage)

@app.route('/deposit', methods=['GET'])
def deposit():
    return render_template('deposit.html')

@app.route('/deposit', methods=['POST'])
def deposit_post():
    document = request.form['document']
    value = float(request.form['value'])
    try:
        bankAccount = logic.deposit(document, value)    
        return render_template('deposit.html', bankAccount=bankAccount)
    except Exception as ex:
        errorMessage = 'Erro interno.'
        if str(ex) == 'BankAccount_NotFound':
            errorMessage = 'Conta bancária não encontrada.'
        if(str(ex) == 'Negative_Value'):
            errorMessage = 'Valor do deposito precisa ser maior que zero.'                    
        return render_template('deposit.html', error=errorMessage)

@app.route('/bankstatement', methods=['GET'])
def bankstatement():
    document = request.args.get(key='document')
    start = request.args.get(key='start')
    end = request.args.get(key='end')
    
    if(document and start and end):
        movements = logic.get_bank_statement(document, start, end)
        movementsModel = list(map(to_movement_model, movements))
        totalDeposits = sum(item.value for item in movementsModel if item.type == 'deposit')
        totalWithdraw = sum(item.value for item in movementsModel if item.type == 'withdraw')
        totalFee = sum(item.value for item in movementsModel if item.type == 'fee')
        return render_template('bankstatement.html', document=document, start=start, end=end, deposits=totalDeposits, withdraws=totalWithdraw, fees=totalFee, movements=movementsModel)
    
    return render_template('bankstatement.html')

def to_movement_model(movement):
    return MovementModel(movement.date, movement.value, movement.movement_type.type)

@app.route('/bankAccount/<document>', methods=['GET'])
def getBankAccountByDocument(document):
    bankAccount = logic.get_bankaccount_by_document_or_error(document=document)
    return make_response(json.dumps({ 'balance': bankAccount.balance, 'name': bankAccount.customer.name}), 200, default_headers())

def default_headers():
    return {"Content-Type": "application/json"}