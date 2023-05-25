from logic.repositories import UserRepository
from loguru import logger
from logic.datavalidation import DataValidation
from logic.entities import User


class UserService:
    def __init__(self):
        self.user_repository = UserRepository()

    def register_user(self, login, password, confirm_password):
        logger.info(f"User with login {login} wants to register")

        if not DataValidation.is_passwords_are_same(password, confirm_password):
            return False, "Passwords don't match"
        logger.info(f"Passwords match")
        if self.is_user_exists(login):
            return False, "Such user has already been created"
        else:
            logger.info(f"New user creation...")
            user = User(login=login, password=DataValidation.encode_password(password))
            logger.info(f"Entity with login = {login} created")
            self.user_repository.create_user(user)
        return True, "Successfully registered"

    def login_user(self, login, password):
        logger.info(f"User with login {login} wants to login.")

        if self.is_user_exists(login):
            user = self.user_repository.get_user_by_login(login)
            logger.info(f"User with {login} found.")
            if DataValidation.is_password_valid(user.password, password):
                user_db = self.user_repository.get_user_by_login(login)
                return user_db, "Successfully logged in"
            else:
                return False, "Incorrect password"
        else:
            return False, f"User with login {login} don't exist"

    def is_user_exists(self, login):
        user = self.user_repository.get_user_by_login(login)
        if user:
            return True
        else:
            return False
