from datasource import DataSource
from datavalidation import DataValidation
from mysql.connector.errors import IntegrityError
from loguru import logger


class UserRepository:
    def __init__(self):
        logger.add("logs/application.log", rotation="500 MB", level="INFO")
        self.connection = DataSource.get_connection()
        self.cursor = self.connection.cursor()

    def register_user(self, login, password, confirm_password):
        logger.info("User with login '{}' wants to register".format(login))

        if not DataValidation.is_password_valid(password, confirm_password):
            logger.info("Passwords and confirm password do not match")
            return False, "Passwords and confirm password do not match"

        if self.is_user_exists(login):
            logger.info("Such user has already been created")
            return False, "Such user has already been created"
        else:
            logger.info("Execute query")
            self.cursor.execute("INSERT INTO user (login, password) VALUES (?, ?)", (login, password))
        return True


    def login_user(self, login, password):
        logger.info("User with login '{}' wants to login".format(login))

        if self.is_user_exists(login):
            user = self.get_user_by_login(login)
            if user[2] == password:
                logger.info("Successfully logged in")
                return True
            else:
                logger.info("Wrong password")
                return False
        else:
            logger.info("User dont exist")

    def get_user_by_login(self, login):
        self.cursor.execute("SELECT * FROM user WHERE login = ?", (login,))
        return self.cursor.fetchone()

    def is_user_exists(self, login):
        user = self.get_user_by_login(login)
        logger.info("user", user)
        if user:
            return True
        else:
            return False
