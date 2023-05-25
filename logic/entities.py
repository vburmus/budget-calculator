import datetime


class User:
    def __init__(self, login: str, password: str, id: int = None, balance: float = 0.0) -> None:
        self._id = id
        self._login = login
        self._password = password
        self._balance = balance

    @property
    def id(self):
        return self._id

    @property
    def login(self):
        return self._login

    @property
    def password(self):
        return self._password

    @property
    def balance(self):
        return self._balance


class Account:
    def __init__(self, name: str, user: User, balance: float = 0.0, id: int = None, description: str = None) -> None:
        self._id = id
        self._name = name
        self._description = description
        self._user = user
        self._balance = balance

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def description(self):
        return self._description

    @property
    def user(self):
        return self._user

    @property
    def balance(self):
        return self._balance


class Type:
    def __init__(self, id: int = 1, name: str = 'income'):
        self._id = id
        self._name = name

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name


class Category:
    def __init__(self, name: str, id: int = None):
        self._id = id
        self._name = name

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name


class Transaction:
    def __init__(self, amount: float, account: Account, id: int = None, description: str = None,
                 date: datetime = datetime.datetime.now(), type: Type = Type(), category: Category = None) -> None:
        self._id = id
        self._account = account
        self._amount = amount
        self._date = date
        self._type = type
        self._category = category
        self._description = description

    @property
    def id(self):
        return self._id

    @property
    def amount(self):
        return self._amount

    @property
    def account(self):
        return self._account

    @property
    def description(self):
        return self._description

    @property
    def date(self):
        return self._date

    @property
    def type(self):
        return self._type

    @property
    def category(self):
        return self._category

    @property
    def user(self):
        return self._account.user
