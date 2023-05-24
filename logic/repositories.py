from logic.datasource import DataSource
from logic.entities import User
from loguru import logger


class UserRepository:
    def __init__(self):
        logger.add("logs/application.log", rotation="500 MB", level="INFO")
        self.connection = DataSource.get_connection()
        self.cursor = self.connection.cursor()

    def register_user(self, user):
        return self.cursor.execute("INSERT INTO user (login, password) VALUES (?, ?)", (user.login, user.password))

    def get_user_by_login(self, login):
        self.cursor.execute("SELECT * FROM user WHERE login = ?", (login,))

        user = self.cursor.fetchone()

        return user

    def get_current_user_balance(self, user):
        return self.cursor.execute("SELECT balance FROM user WHERE login = ?", (user.login,))


class AccountRepository:
    def __init__(self):
        logger.add("logs/application.log", rotation="500 MB", level="INFO")
        self.connection = DataSource.get_connection()
        self.cursor = self.connection.cursor()


class TransactionRepository:
    def __init__(self):
        logger.add("logs/application.log", rotation="500 MB", level="INFO")
        self.connection = DataSource.get_connection()
        self.cursor = self.connection.cursor()


class СategoryRepository:
    def __init__(self):
        logger.add("logs/application.log", rotation="500 MB", level="INFO")
        self.connection = DataSource.get_connection()
        self.cursor = self.connection.cursor()
