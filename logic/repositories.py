from abc import ABC, abstractmethod
from enum import Enum
from typing import TypeVar, Generic, Any, List

from logic.datasource import DataSource
from loguru import logger

from logic.entities import User, Account, Category, Type, Transaction

DELETE_TRANSACTION_QUERY = "DELETE FROM transaction WHERE id = ?"

UPDATE_TRANSACTION_QUERY = "UPDATE transaction SET amount = ?, description = ?," \
                           "date = CURRENT_TIMESTAMP,  type_id = ?, category_id = ? WHERE id = ?"

UPDATE_TYPE_QUERY = "UPDATE type SET name = ? WHERE id = ?"

DELETE_TYPE_QUERY = "DELETE FROM type WHERE id = ?"

UPDATE_CATEGORY_QUERY = "UPDATE category SET name = ? WHERE id = ?"

DELETE_CATEGORY_QUERY = "DELETE FROM category  WHERE id = ?"

DELETE_ACCOUNT_QUERY = "DELETE FROM account WHERE id=? "

UPDATE_USER_QUERY = "UPDATE user SET login = ?, password = ? WHERE id = ?"

SELECT_TRANSACTIONS_BY_ACCOUNT_TYPE_CATEGORY_QUERY = "SELECT * FROM transaction " \
                                                     "WHERE account_id = ? and type_id = ? and category_id = ? "

SELECT_TRANSACTIONS_BY_ACCOUNT_TYPE_QUERY = "SELECT * FROM transaction WHERE account_id = ? and type_id = ?"

SELECT_TRANSACTIONS_BY_ACCOUNT_QUERY = "SELECT * FROM transaction WHERE account_id = ?"

SELECT_TRANSACTION_BY_ID_QUERY = "SELECT * FROM transaction WHERE id = ?"

CREATE_TRANSACTION_QUERY = "INSERT INTO transaction" \
                           " (amount, description, account_id, type_id, category_id) VALUES (?,?,?,?,?)"

GET_TYPE_BY_ID_QUERY = "SELECT * FROM type WHERE id = ?  "

CREATE_TYPE_QUERY = "INSERT INTO type (name) VALUES (?)"

GET_CATEGORY_BY_ID_QUERY = "SELECT * FROM category WHERE id = ?  "

CREATE_CATEGORY_QUERY = "INSERT INTO category (name) VALUES (?)"

GET_CURRENT_USER_BALANCE_QUERY = "SELECT balance FROM user WHERE login = ?"

DELETE_USER_QUERY = "DELETE FROM user WHERE login = ?)"

GET_USER_BY_ID_QUERY = "SELECT * FROM user WHERE id = ?"

GET_USER_BY_LOGIN_QUERY = "SELECT * FROM user WHERE login = ?"

CREATE_USER_QUERY = "INSERT INTO user (login, password) VALUES (?, ?)"

CREATE_ACCOUNT_QUERY = "INSERT INTO account (name,description, balance, user_id) VALUES (?, ?, ?, ?)"

GET_ACCOUNTS_BY_USER_QUERY = "SELECT * FROM account where user_id = ?"

GET_ACCOUNT_BY_ID_QUERY = "SELECT * FROM account WHERE id = ?"

UPDATE_ACCOUNT_QUERY = "UPDATE account SET name = ?, description = ?, user_id = ?, balance = ? WHERE  id = ?"

LAST_ROW_QUERY = "SELECT * FROM '{}' ORDER BY id DESC LIMIT 1"


class ParamType(Enum):
    ID = 1,
    LOGIN = 2,
    User = 3,


T = TypeVar('T')


class ARepository(Generic[T], ABC):

    def __init__(self):
        logger.add("logs/application.log", rotation="500 MB", level="INFO")
        self.connection = DataSource.get_connection()
        self.cursor = self.connection.cursor()

    @abstractmethod
    def create(self, item: T) -> T:
        pass

    @abstractmethod
    def get_by_param(self, item: Any) -> T | List[T]:
        pass

    @abstractmethod
    def update(self, item: T) -> T:
        pass

    @abstractmethod
    def delete(self, item: T) -> None:
        pass

    def get_last_row(self, table) -> T:
        self.cursor.execute(LAST_ROW_QUERY.format(table))
        result = self.cursor.fetchone()
        item = self.parse(result)
        return item

    @staticmethod
    @abstractmethod
    def parse(item_representation: str) -> T | None:
        pass


class UserRepository(ARepository[User]):

    def create(self, user: User) -> User:
        self.cursor.execute(CREATE_USER_QUERY, (user.login, user.password))
        return self.get_last_row("user")

    def get_by_param(self, param: str | int) -> User | None:

        if isinstance(param, int):
            self.cursor.execute(GET_USER_BY_ID_QUERY, (param,))
        elif isinstance(param, str):
            self.cursor.execute(GET_USER_BY_LOGIN_QUERY, (param,))
        else:
            logger.error(f"There is no  such option for this type")
            return None
        result = self.cursor.fetchone()
        user = self.parse(result)
        logger.info(result)
        return user

    def update(self, user: User) -> User:
        old_user = self.get_by_param(user.login)
        self.cursor.execute(UPDATE_USER_QUERY, (user.id,))
        return self.get_by_param(old_user.id)

    def delete(self, user: User) -> None:
        return self.cursor.execute(DELETE_USER_QUERY, (user.login,))

    @staticmethod
    def parse(user: str) -> User | None:
        if user is None:
            return None
        return User(id=int(user[0]), login=user[1], password=user[2], balance=float(user[3]))


class AccountRepository(ARepository[Account]):

    def create(self, account: Account) -> Account:
        self.cursor.execute(CREATE_ACCOUNT_QUERY,
                            (account.name, account.description, account.balance, account.user.id))

        return self.get_last_row("account")

    def get_by_param(self, item: User | int) -> Account | List[Account] | None:
        if isinstance(item, User):
            self.cursor.execute(GET_ACCOUNTS_BY_USER_QUERY, (item.id,))
            result = self.cursor.fetchall()
            accounts = []

            for account in result:
                accounts.append(self.parse(account))
            return accounts
        elif isinstance(item, int):
            self.cursor.execute(GET_ACCOUNT_BY_ID_QUERY, (id,))
        else:
            logger.error(f"There is no such option for this type")
            return None
        result = self.cursor.fetchone()
        account = self.parse(result)
        return account

    def update(self, account: Account) -> Account:
        self.cursor.execute(UPDATE_ACCOUNT_QUERY, (
            account.name, account.description, account.user.id, account.balance, account.id,))
        return self.get_by_param(account.id)

    def delete(self, account: Account) -> None:
        self.cursor.execute(DELETE_ACCOUNT_QUERY, (account.id,))

    @staticmethod
    def parse(account: str) -> Account | None:
        if account is None:
            return None
        user_repository = UserRepository()
        user = user_repository.get_by_param(int(account[4]))
        return Account(id=int(account[0]), name=account[1], balance=float(account[2]),
                       description=account[3], user=user)


class CategoryRepository(ARepository[Category]):

    def create(self, category: Category) -> Category:
        self.cursor.execute(CREATE_CATEGORY_QUERY, (category.name,))
        return self.get_last_row("category")

    def get_by_param(self, id: int) -> Category:
        self.cursor.execute(GET_CATEGORY_BY_ID_QUERY, (id,))
        result = self.cursor.fetchone()
        user = self.parse(result)
        logger.info(result)
        return user

    def update(self, category: Category) -> Category:
        self.cursor.execute(UPDATE_CATEGORY_QUERY, (category.name, category.id,))
        return self.get_by_param(category.id)

    def delete(self, category: Category) -> None:
        self.cursor.execute(DELETE_CATEGORY_QUERY, (category.id,))

    @staticmethod
    def parse(category: str) -> Category | None:
        if category is None:
            return None
        return Category(id=int(category[0]), name=category[1])


class TypeRepository(ARepository[Type]):
    def create(self, type: Type) -> Type:
        self.cursor.execute(CREATE_TYPE_QUERY, (type.name,))
        return self.get_last_row("type")

    def get_by_param(self, item: int) -> Type:
        self.cursor.execute(GET_TYPE_BY_ID_QUERY, (id,))
        result = self.cursor.fetchone()

        type = self.parse(result)
        logger.info(result)
        return type

    def update(self, type: Type) -> Type:
        self.cursor.execute(UPDATE_TYPE_QUERY, (type.name, type.id,))
        return self.get_by_param(type.id)

    def delete(self, type: Type) -> None:
        self.cursor.execute(DELETE_TYPE_QUERY, (type.id,))

    @staticmethod
    def parse(type: str) -> T | None:
        if type is None:
            return None
        return Type(id=int(type[0]), name=type[1])


class TransactionRepository(ARepository[Transaction]):
    def create(self, transaction: Transaction) -> Transaction:
        self.cursor.execute(
            CREATE_TRANSACTION_QUERY, (transaction.amount,
                                       transaction.description,
                                       transaction.account.id,
                                       transaction.type.id,
                                       transaction.category.id))
        return self.get_last_row("transaction")

    def get_by_param(self, item: int | Account) -> Transaction | List[Transaction]:
        if isinstance(item, int):
            self.cursor.execute(SELECT_TRANSACTION_BY_ID_QUERY, (id,))
            result = self.cursor.fetchone()
            transaction = self.parse(result)
            return transaction
        elif isinstance(item, Account):
            self.cursor.execute(SELECT_TRANSACTIONS_BY_ACCOUNT_QUERY, (item.id,))
            result = self.cursor.fetchall()
            transactions = []

            for transaction in result:
                transactions.append(self.parse(transaction))
            return transactions

    def update(self, transaction: Transaction) -> Transaction:
        self.cursor.execute(UPDATE_TRANSACTION_QUERY, (transaction.amount,
                                                       transaction.description,
                                                       transaction.type.id,
                                                       transaction.category.id))
        return self.get_by_param(transaction.id)

    def delete(self, transaction: Transaction) -> None:
        self.cursor.execute(DELETE_TRANSACTION_QUERY, (transaction.id,))

    @staticmethod
    def parse(transaction: str) -> Transaction | None:
        if transaction is None:
            return None
        category_repository = CategoryRepository()
        type_repository = TypeRepository()
        account_repository = AccountRepository()
        category = category_repository.get_by_param(int(transaction[6]))
        type = type_repository.get_by_param(int(transaction[5]))
        account = account_repository.get_by_param(int(transaction[4]))
        return Transaction(id=int(transaction[0]), amount=float(transaction[1]), description=transaction[2],
                           date=transaction[3], account=account, type=type, category=category)
