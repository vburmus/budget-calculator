from typing import List

from logic.repositories import UserRepository, AccountRepository, CategoryRepository, UserHasCategoryRepository, \
    TransactionRepository
from loguru import logger
from logic.datavalidation import DataValidation
from logic.entities import User, Account, Category, UserCategory, Transaction


class UserService:
    def __init__(self):
        self.user_repository = UserRepository()
        self.user_category_repository = UserHasCategoryRepository()
        self.category_service = CategoryService()

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
    def update(self, user: User, given_password: str, login: str = None, password: str = None):
        bd_user = self.get_user_by_id(user.id)
        logger.info(f"Update user {user.login}...")
        logger.info(f"{DataValidation.encode_password(given_password)} == {user.password}")
        if not DataValidation.is_password_valid(bd_user.password,
                                                given_password):
            return False, "Given password is wrong"
        if login:
            if login == user.login:
                return False, "Credentials must be changed to update"
            if self.is_user_exists(login):
                return False, "Such login is unavailable"
            user.login = login
            logger.info("Login updated")
        if password:
            if DataValidation.is_password_valid(bd_user.password,
                                                password):
                return False, "Credentials must be changed to update"
            user.password = DataValidation.encode_password(password)
            logger.info("Password updated")
        if login or password:
            return True, self.user_repository.update(user)
        return False, "Empty credentials"

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

    def get_user_categories(self, user: User) -> List[Category]:
        logger.info("Getting user repositories...")
        return self.user_category_repository.get_by_param(user)

    def is_user_has_category(self, user: User, category: Category) -> bool:
        user_categories_names = [category.name for category in self.get_user_categories(user)]
        if category.name in any(user_categories_names):
            return True
        else:
            return False

    def add_category_user(self, user: User, name: str):
        category = Category(name=name)
        if self.is_user_has_category(user, category):
            return False, f"Category {category.name} exists"
        if self.category_service.is_category_exist(category.name):
            category.id = self.category_service.get_category_by_name(name).id
            return True, self.user_category_repository.create(
                UserCategory(user=user, category=category))
        else:
            success, message = self.category_service.create(category.name)
            if success:
                return True, self.user_category_repository.create(UserCategory(user=user, category=success))
            return False, message

    def delete_category_from_user(self, user: User, name: str):

        if not self.category_service.is_category_exist(name):
            return False, "There is no such category"
        category = Category(name=name)
        if not self.is_user_has_category(user=user, category=category):
            return False, "Wrong category"
        else:
            category = self.category_service.get_category_by_name(name)
            user_category = UserCategory(user=user, category=category)
            self.user_category_repository.delete(user_category)

            if self.category_service.get_category_count(category) == 0:
                self.category_service.delete(category)
            return True, f"Successfully deleted {category.name}"


class AccountService:

    def __init__(self):
        self.account_repository = AccountRepository()
        self.transaction_repository = TransactionRepository()

    def create(self, name: str, user: User, balance: str = "0", description: str = ""):
        if not name:
            return False, "Name can't be null "
        if not DataValidation.isfloat(balance):
            return False, f"Wrong format of balance"
        current = float(balance)
        logger.info(f"Creating account with name {name}...")
        if self.is_account_exists(name, user):
            return False, f"Account {name} exists"
        account = Account(name=name, user=user, balance=current, description=description)
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
            correction = balance - account.balance

            success, _ = self.transaction_repository.create(
                Transaction(amount=correction, account=account, description="Correction"))
            if not success:
                return False, "Error while correcting"

            logger.info("Balance updated")

        return True, self.account_repository.update(account)

    def delete(self, account: Account):
        if not self.is_account_exists(account.name, account.user):
            return False, f"Account {account.name} doesn't exist"
        self.delete(account)
        return True, f"Account {account.name} successfully deleted"

    def is_account_exists(self, name: str, user: User) -> bool:
        user_accounts_names = []
        for account in self.account_repository.get_by_param(user):
            user_accounts_names.append(account.name)
        if len(user_accounts_names) == 0:
            return False
        if name in user_accounts_names:
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

        return True, self.category_repository.create(category)

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


class TransactionService():
    def __init__(self):
        self.transaction_repository = TransactionRepository()

    def create(self, amount: str, description: str, account: Account, category: Category):
        logger.info(f"Creating transaction...")
        if not amount:
            return False, f"Amount can't be null"
        if not DataValidation.isfloat(amount):
            return False, "Amount must be float"

        transaction = Transaction(amount=float(amount), account=account, description=description, category=category)
        return True, self.transaction_repository.create(transaction)
