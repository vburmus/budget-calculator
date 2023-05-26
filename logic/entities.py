import datetime


class User:
    def __init__(self, login: str, password: str, id: int = None, balance: float = 0.0) -> None:
        self._id = id
        self._login = login
        self._password = password
        self._balance = balance

    @property
    def id(self) -> int:
        return self._id

    @id.setter
    def id(self, new_id: int) -> None:
        self._id = new_id

    @property
    def login(self) -> str:
        return self._login

    @login.setter
    def login(self, new_login: str) -> None:
        self._login = new_login

    @property
    def password(self) -> str:
        return self._password

    @password.setter
    def password(self, new_password: str) -> None:
        self._password = new_password

    @property
    def balance(self) -> float:
        return self._balance

    @balance.setter
    def balance(self, new_balance: float) -> None:
        self._balance = new_balance


class Account:
    def __init__(self, name: str, user: User, balance: float = 0.0, id: int = None, description: str = None) -> None:
        self._id = id
        self._name = name
        self._description = description
        self._user = user
        self._balance = balance

    @property
    def id(self) -> int:
        return self._id

    @id.setter
    def id(self, new_id: int) -> None:
        self._id = new_id

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, new_name: str) -> None:
        self._name = new_name

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, new_description: str) -> None:
        self._description = new_description

    @property
    def user(self) -> User:
        return self._user

    @user.setter
    def user(self, new_user: User) -> None:
        self._user = new_user

    @property
    def balance(self) -> float:
        return self._balance

    @balance.setter
    def balance(self, new_balance: float) -> None:
        self._balance = new_balance




class Category:
    def __init__(self, name: str, id: int = None):
        self._id = id
        self._name = name

    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @id.setter
    def id(self, new_id: int) -> None:
        self._id = new_id

    @name.setter
    def name(self, new_name: str) -> None:
        self._name = new_name


class Transaction:
    def __init__(self, amount: float, account: Account, id: int = None, description: str = None,
                 date: datetime = datetime.datetime.now(), category: Category = None) -> None:
        self._id = id
        self._account = account
        self._amount = amount
        self._date = date
        self._category = category
        self._description = description

    @property
    def id(self) -> int:
        return self._id

    @id.setter
    def id(self, new_id: int) -> None:
        self._id = new_id

    @property
    def amount(self) -> float:
        return self._amount

    @amount.setter
    def amount(self, new_amount: float) -> None:
        self._amount = new_amount

    @property
    def account(self) -> Account:
        return self._account

    @account.setter
    def account(self, new_account: Account) -> None:
        self._account = new_account

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, new_description: str) -> None:
        self._description = new_description

    @property
    def date(self) -> datetime:
        return self._date

    @date.setter
    def date(self, new_date: datetime) -> None:
        self._date = new_date


    @property
    def category(self) -> Category:
        return self._category

    @category.setter
    def category(self, new_category: Category) -> None:
        self._category = new_category

    @property
    def user(self):
        return self._account.user

