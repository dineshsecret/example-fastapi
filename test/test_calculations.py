# pytest -v -s - x
import pytest
from app.calculation import BankAccount, add,subtract,multipy,divide,InsufficientFunds

@pytest.fixture
def zero_bank_account():
    print("creating empty bank account")
    return BankAccount()

@pytest.fixture
def bank_account():
    return BankAccount(50)
    
@pytest.mark.parametrize("x,y,expected",[
    (3,2,5),
    (4,1,5),
    (5,2,7),
    (5,-3,2),
])

def test_add(x,y,expected):
    assert add(x,y) == expected

def test_add1():
    print("testing add function")
    assert add(5,3) == 8


def test_add2():    
    assert add(4,1) == 5
    
def test_add3():
    print("testing add function")
    assert add(5,2) == 7
    
def test_add4():
    print("testing add function")
    assert add(5,-3) == 2

def test_subtract():
    assert subtract(10,8)==2

def test_multiply():
    assert multipy(2,5) == 10

def test_divide():
    assert(8/2)==4

def test_bank_set_initial_amount(bank_account):
    
    assert bank_account.balance == 50

def test_bank_default_amount(zero_bank_account): # fixture being set as argument
    print("testing my bank account")
    assert zero_bank_account.balance==0

def test_withdraw(bank_account):
    
    bank_account.withdraw(20)
    assert bank_account.balance == 30

def test_deposit(bank_account):
   
    bank_account.deposit(30)
    assert bank_account.balance == 80

def test_collect_interest(bank_account):
    bank_account.collect_interest()
    assert round(bank_account.balance,5) == 55

@pytest.mark.parametrize("deposited,withdrew,expected",[
    (200,100,100),
    (50,10,40),
    (1200,200,1000)
])
def test_bank_transaction_param(zero_bank_account,deposited,withdrew,expected):
    zero_bank_account.deposit(deposited)
    zero_bank_account.withdraw(withdrew)
    assert zero_bank_account.balance == expected

def test_bank_transaction(zero_bank_account):
    zero_bank_account.deposit(200)
    zero_bank_account.withdraw(100)
    assert zero_bank_account.balance == 100

def test_insufficient_fund(bank_account):
    with pytest.raises(InsufficientFunds):
        bank_account.withdraw(200)