from logic.repositories import UserRepository, AccountRepository, CategoryRepository
from loguru import logger
from logic.datavalidation import DataValidation
from logic.entities import User, Account, Category


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
        if login == user.login:
            return False, "Credentials must be changed to update"

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


class AccountService:

    def __init__(self):
        self.account_repository = AccountRepository()

    def create(self, name: str, user: User, balance: float = 0.0, description: str = ""):
        logger.info(f"Creating account with name {name}...")
        if self.is_account_exists(name, user):
            return False, f"Account {name} exists"
        account = Account(name=name, user=user, balance=balance, description=description)
        self.account_repository.create(account)
        return True, f"Successfully created account {name}"

    def get_user_accounts(self, user: User):
        return self.account_repository.get_by_param(user)

    def get_account_by_id(self, id: int):
        return self.account_repository.get_by_param(id)

    def update(self, account: Account, name: str, description: str, balance: float):
        if account.name == name and account.description == description and account.balance == balance:
            return False, "Credentials must be changed to update"
        logger.info("Updating account...")
        if name:
            if self.is_account_exists(name, account.user):
                return False, "Account with name {name} exist"
            account.name = name
            logger.info("Name updated")
        if description:
            account.description = description
            logger.info("Description updated")
        if balance:
            account.balance = balance
            logger.info("Balance updated")

        return True, self.account_repository.update(account)

    def delete(self, account: Account):
        if not self.is_account_exists(account.name, account.user):
            return False, f"Account {account.name} doesn't exist"
        self.delete(account)
        return True, f"Account {account.name} successfully deleted"

    def is_account_exists(self, name: str, user: User) -> bool:
        accounts = self.account_repository.get_by_param(user)
        if name in any(accounts.name):
            return True
        else:
            return False


class CategoryService:

    def __init__(self):
        self.category_repository = CategoryRepository()

    def create(self, name):
        logger.info(f"Creating category with name {name}...")
        if self.is_category_exist(name):
            return False, f"Category {name} exists"
        category = Category(name)
        self.category_repository.create(category)
        return True, f"Successfully created category {name}"

    def get_category_by_id(self, id: int):
        return self.category_repository.get_by_param(id)

    def get_account_by_name(self, name: str):
        return self.category_repository.get_by_param(name)

    def update(self, category: Category, name: str):
        logger.info(f"Update category {category.name}...")
        if category.name == name:
            return False, "Credentials must be changed to update"
        if name:
            if self.is_category_exist(name):
                return False, "Such name is unavailable"
            category.name = name
            logger.info("Name updated")

        return True, self.category_repository.update(category)

    def delete(self, category: Category):
        if not self.is_category_exist(category.name):
            return False, f"Category {category.name} doesn't exist"
        self.delete(category)
        return True, f"Category {category.name} successfully deleted"

    def is_category_exist(self, name: str) -> bool:
        category = self.category_repository.get_by_param(name)
        if category:
            return True
        else:
            return False