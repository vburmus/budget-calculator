from logic.repositories import UserRepository, ARepository, AccountRepository
from loguru import logger
from logic.datavalidation import DataValidation
from logic.entities import User, Account


class UserService:
    def __init__(self):
        self.user_repository = UserRepository()

    def register(self, login: str, password: str, confirm_password: str):
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
            self.user_repository.create(user)
        return True, f"Successfully registered {login}"

    def login(self, login: str, password: str):
        logger.info(f"User with login {login} wants to login.")

        if self.is_user_exists(login):
            user = self.user_repository.get_by_param(login)
            logger.info(f"User with {login} found.")
            if DataValidation.is_password_valid(user.password, password):
                user_db = self.user_repository.get_by_param(login)
                return user_db, "Successfully logged in"
            else:
                return False, "Incorrect password"
        else:
            return False, f"User with login {login} don't exist"

    def get_user_by_id(self, id: int):
        logger.info(f"Searching user with id = {id} ")
        return self.user_repository.get_by_param(id)

    def get_user_by_login(self, login: str):
        logger.info(f"Searching user with login = {login} ")
        return self.user_repository.get_by_param(login)

    # Response of this method should be handled in the ui side and logger
    # WARNING TYPE IF FALSE
    # if we can update we return True + user
    # if not -> false + message
    def update(self, user: User, login: str = None, password: str = None):
        logger.info(f"Update user {user.login}...")
        if login:
            if self.is_user_exists(login):
                return False, "Such login is unavailable"
            user.login = login
            logger.info("Login updated")
        if password:
            user.password = DataValidation.encode_password(password)
            logger.info("Password updated")
        return True, self.user_repository.update(user)

    # +- -||- HANDLE LOGS!
    def delete(self, user: User):
        logger.info(f"Deleting user {user.login}...")
        if not self.is_user_exists(user.login):
            return False, f"User {user.login} doesn't exist"
        self.delete(user)
        return True, f"User {user.login} successfully deleted"

    def is_user_exists(self, login: str) -> bool:
        user = self.user_repository.get_by_param(login)
        if user:
            return True
        else:
            return False
