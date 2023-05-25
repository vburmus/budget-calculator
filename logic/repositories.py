from logic.datasource import DataSource
from loguru import logger

from logic.entities import User, Account, Category

GET_CURRENT_USER_BALANCE_QUERY = "SELECT balance FROM user WHERE login = ?"

DELETE_USER_QUERY = "DELETE FROM user WHERE login = ?)"

GET_USER_BY_ID_QUERY = "SELECT * FROM user WHERE id = ?"

GET_USER_BY_LOGIN_QUERY = "SELECT * FROM user WHERE login = ?"

CREATE_USER_QUERY = "INSERT INTO user (login, password) VALUES (?, ?)"

CREATE_ACCOUNT_QUERY = "INSERT INTO account (name,description, balance, user_id) VALUES (?, ?, ?, ?)"

GET_ACCOUNTS_BY_USER_QUERY = "SELECT * FROM account where user_id = ?"

GET_ACCOUNT_BY_ID_QUERY = "SELECT * FROM account WHERE id = ?"

UPDATE_ACCOUNT_QUERY = "UPDATE account SET name = ?, description = ?, user_id = ?, balance = ? WHERE  id = ?"


class UserRepository:
    def __init__(self):
        logger.add("logs/application.log", rotation="500 MB", level="INFO")
        self.connection = DataSource.get_connection()
        self.cursor = self.connection.cursor()

    def create_user(self, user: User):
        return self.cursor.execute(CREATE_USER_QUERY, (user.login, user.password))

    def get_user_by_login(self, login):
        self.cursor.execute(GET_USER_BY_LOGIN_QUERY, (login,))
        result = self.cursor.fetchone()

        user = self.parse_user(result)
        logger.info(result)
        return user

    def get_user_by_id(self, id):
        self.cursor.execute(GET_USER_BY_ID_QUERY, (id,))
        result = self.cursor.fetchone()

        user = self.parse_user(result)
        logger.info(result)
        return user

    def get_current_user_balance(self, user: User):
        return self.cursor.execute(GET_CURRENT_USER_BALANCE_QUERY, (user.login,))

    def delete_user(self, user: User):
        return self.cursor.execute(DELETE_USER_QUERY, (user.login,))

    @staticmethod
    def parse_user(user):
        if user is None:
            return None
        return User(id=user[0], login=user[1], password=user[2], balance=float(user[3]))


class AccountRepository:
    def __init__(self):
        logger.add("logs/application.log", rotation="500 MB", level="INFO")
        self.connection = DataSource.get_connection()
        self.cursor = self.connection.cursor()

    def create_new_account(self, account: Account):
        return self.cursor.execute(CREATE_ACCOUNT_QUERY,
                                   (account.name, account.description, account.balance, account.user.id))

    def get_accounts_by_user(self, user: User):
        self.cursor.execute(GET_ACCOUNTS_BY_USER_QUERY, (user.id,))
        result = self.cursor.fetchall()
        accounts = []

        for account in result:
            accounts.append(self.parse_account(account))
        return accounts

    def get_account_by_id(self, id):
        self.cursor.execute(GET_ACCOUNT_BY_ID_QUERY, (id,))
        result = self.cursor.fetchone()
        account = self.parse_account(result)
        return account

    def update_account(self, account: Account):
        self.cursor.execute(UPDATE_ACCOUNT_QUERY, (
            account.name, account.description, account.user.id, account.balance, account.id,));

    @staticmethod
    def parse_account(account: Account):
        if account is None:
            return None
        user_repository = UserRepository()
        user = user_repository.get_user_by_id(account[4])
        return Account(id=account[0], name=account[1], balance=account[2],
                       description=account[3], user=user)


class СategoryRepository:
    def __init__(self):
        logger.add("logs/application.log", rotation="500 MB", level="INFO")
        self.connection = DataSource.get_connection()
        self.cursor = self.connection.cursor()

    def create_category(self, category: Category):
        self.cursor.execute("INSERT INTO category (name) VALUES (?)", (category.name,))

    def get_category_by_id(self, id):
        self.cursor.execute("SELECT * FROM category WHERE id = ?  ", (id,))
        result = self.cursor.fetchone()

        user = self.parse_user(result)
        logger.info(result)
        return user


class TypeRepository:
    def __init__(self):
        logger.add("logs/application.log", rotation="500 MB", level="INFO")
        self.connection = DataSource.get_connection()
        self.cursor = self.connection.cursor()


class TransactionRepository:
    def __init__(self):
        logger.add("logs/application.log", rotation="500 MB", level="INFO")
        self.connection = DataSource.get_connection()
        self.cursor = self.connection.cursor()
