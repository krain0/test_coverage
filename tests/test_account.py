"""
Test Cases TestAccountModel
"""
import json
from random import randrange
import pytest
from models import db, app
from models.account import Account, DataValidationError

ACCOUNT_DATA = {}

@pytest.fixture(scope="module", autouse=True)
def load_account_data():
    """ Load data needed by tests """
    global ACCOUNT_DATA
    with open('tests/fixtures/account_data.json') as json_data:
        ACCOUNT_DATA = json.load(json_data)

    # Set up the database tables
    db.create_all()
    yield
    db.session.close()

@pytest.fixture(scope="function", autouse=True)
def setup_and_teardown():
    """ Truncate the tables and set up for each test """
    db.session.query(Account).delete()
    db.session.commit()
    yield
    db.session.remove()

######################################################################
#  T E S T   C A S E S
######################################################################

def test_create_all_accounts():
    """ Test creating multiple Accounts """
    for data in ACCOUNT_DATA:
        account = Account(**data)
        account.create()
    assert len(Account.all()) == len(ACCOUNT_DATA)

def test_create_an_account():
    """ Test Account creation using known data """
    rand = randrange(0, len(ACCOUNT_DATA))
    data = ACCOUNT_DATA[rand]  # get a random account
    account = Account(**data)
    account.create()
    assert len(Account.all()) == 1


# ADDED
def test_repr():
    """Test the representation of an account"""
    account = Account()
    account.name = "Foo"
    assert str(account) == "<Account 'Foo'>"

def test_to_dict():
    """ Test account to dict """
    rand = randrange(0, len(ACCOUNT_DATA))  # Generate a random index
    data = ACCOUNT_DATA[rand]  # get a random account
    account = Account(**data)
    result = account.to_dict()

    assert account.name == result["name"]
    assert account.email == result["email"]
    assert account.phone_number == result["phone_number"]
    assert account.disabled == result["disabled"]
    assert account.date_joined == result["date_joined"]

def test_from_dict():
    result = dict();
    result["name"] = "John"
    result["email"] = "john@mail.com"
    result["phone_number"] = "1234567"

    account = Account()
    account.from_dict(result)

    assert account.name == result["name"]
    assert account.email == result["email"]
    assert account.phone_number == result["phone_number"]
    # assert account.disabled == result["disabled"]
    # assert account.date_joined == result["date_joined"]


def test_update_withID():
    # creating example info, with an ID
    newAccountInfo = dict()
    newAccountInfo["name"] = "Sam Sam"
    newAccountInfo["email"] = "sam@sam.sam"
    newAccountInfo["phone_number"] = "123.456.789"
    newAccountInfo["disabled"] = False
    newAccountInfo["id"] = 123

    account = Account(**newAccountInfo)
    userId = account.id
    account.create()
    
    newEmail = "sam_" + account.email

    account.email = newEmail
    account.update()
    
    newAccount = Account.find(userId)
    assert newAccount.email == newEmail


def test_update_noID():
    rand = randrange(0, len(ACCOUNT_DATA))  # Generate a random index
    data = ACCOUNT_DATA[rand]  # get a random account
    account = Account(**data)
    try:
        # example data has no ID, so this should throw an exception
        account.update()
        assert False
    except DataValidationError:
        assert True

def test_delete():
    # creating example info, with an ID
    newAccountInfo = dict()
    newAccountInfo["name"] = "Sam Sam"
    newAccountInfo["email"] = "sam@sam.sam"
    newAccountInfo["phone_number"] = "123.456.789"
    newAccountInfo["disabled"] = False
    newAccountInfo["id"] = 123

    account = Account(**newAccountInfo)
    userId = account.id
    account.create()
    assert Account.find(userId) != None # make sure it was created
    account.delete()
    assert Account.find(userId) == None # make sure it is gone
    
