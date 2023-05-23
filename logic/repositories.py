from logic.datasource import DataSource

from loguru import logger


class UserRepository:
    def __init__(self):
        logger.add("logs/application.log", rotation="500 MB", level="INFO")
        self.connection = DataSource.get_connection()
        self.cursor = self.connection.cursor()

    def register_user(self, login, password):
        return self.cursor.execute("INSERT INTO user (login, password) VALUES (?, ?)", (login, password))

    def get_user_by_login(self, login):
        self.cursor.execute("SELECT * FROM user WHERE login = ?", (login,))
        return self.cursor.fetchone()


