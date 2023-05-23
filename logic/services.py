from logic.repositories import UserRepository
from loguru import logger
from logic.datavalidation import DataValidation


class UserService:
    def __init__(self):
        self.user_repository = UserRepository()

    def register_user(self, login, password, confirm_password):
        logger.info("User with login '{}' wants to register".format(login))

        if not DataValidation.is_passwords_are_same(password, confirm_password):
            return False, "Passwords and confirm password do not match"

        if self.is_user_exists(login):
            return False, "Such user has already been created"
        else:
            logger.info("Password encryption")
            encoded_password = DataValidation.encode_password(password)
            self.user_repository.register_user(login,encoded_password)
        return True, "Successfully logged in"

    def login_user(self, login, password):
        logger.info("User with login '{}' wants to login".format(login))

        if self.is_user_exists(login):
            user = self.user_repository.get_user_by_login(login)
            if DataValidation.is_password_valid(user[2], password):
                return True, "Successfully logged in"
            else:
                return False, "Incorrect password"
        else:
            logger.info("User don't exist")
            return False, "User don't exist"

    def is_user_exists(self, login):
        user = self.user_repository.get_user_by_login(login)
        if user:
            return True
        else:
            return False
