from abc import ABC, abstractmethod
from enum import Enum
from typing import TypeVar, Generic, Any, List

from logic.datasource import DataSource
from loguru import logger

from logic.entities import User, Account, Category, Transaction, UserCategory

CREATE_NEW_CATEGORY_QUERY = "insert into user_has_category (user_id, category_id) values (?,?)"

SELECT_USERS_CATEGORIES_QUERY = "select c.id,c.name from user_has_category as u join category as c on u.category_id = c.id  where user_id = ?"

SELECT_CATEGORY_COUNT_QUERY = "select count(*) from user_has_category where category_id = ?"

DELETE_USER_HAS_CATEGORY_QUERY = "delete from user_has_category where user_id = ? and category_id =?"

DELETE_TRANSACTION_QUERY = "DELETE FROM transaction WHERE id = ?"

UPDATE_TRANSACTION_QUERY = "UPDATE transaction SET amount = ?, description = ?," \
                           "date = CURRENT_TIMESTAMP, category_id = ? WHERE id = ?"

UPDATE_CATEGORY_QUERY = "UPDATE category SET name = ? WHERE id = ?"

DELETE_CATEGORY_QUERY = "DELETE FROM category  WHERE id = ?"

DELETE_ACCOUNT_QUERY = "DELETE FROM account WHERE id=? "

UPDATE_USER_QUERY = "UPDATE user SET login = ?, password = ? WHERE id = ?"

SELECT_TRANSACTIONS_BY_ACCOUNT_QUERY = "SELECT t.id,t.amount,t.description,t.date,t.account_id,c.id,c.name FROM transaction as t left join category as c on c.id = t.category_id WHERE account_id = ?"

SELECT_TRANSACTION_BY_ID_QUERY = "SELECT * FROM transaction WHERE id = ?"

CREATE_TRANSACTION_QUERY = "INSERT INTO transaction" \
                           " (amount, description, account_id,category_id) VALUES (?,?,?,?)"

CREATE_TRANSACTION_WITHOUT_CATEGORY_QUERY = "INSERT INTO transaction" \
                                            " (amount, description, account_id) VALUES (?,?,?)"

GET_CATEGORY_BY_ID_QUERY = "SELECT * FROM category WHERE id = ?  "
GET_CATEGORY_BY_NAME_QUERY = "SELECT * FROM category WHERE name = ?  "
CREATE_CATEGORY_QUERY = "INSERT INTO category (name) VALUES (?)"

GET_CURRENT_USER_BALANCE_QUERY = "SELECT balance FROM user WHERE login = ?"

DELETE_USER_QUERY = "DELETE FROM user WHERE login = ?"

GET_USER_BY_ID_QUERY = "SELECT * FROM user WHERE id = ?"

GET_USER_BY_LOGIN_QUERY = "SELECT * FROM user WHERE BINARY login = ?"

CREATE_USER_QUERY = "INSERT INTO user (login, password) VALUES (?, ?)"

CREATE_ACCOUNT_QUERY = "INSERT INTO account (name,description, balance, user_id) VALUES (?, ?, ?, ?)"

GET_ACCOUNTS_BY_USER_QUERY = "SELECT * FROM account where user_id = ?"

GET_ACCOUNT_BY_ID_QUERY = "SELECT * FROM account WHERE id = ?"

UPDATE_ACCOUNT_QUERY = "UPDATE account SET name = ?, description = ?, user_id = ?, balance = ? WHERE  id = ?"

LAST_ROW_QUERY = "SELECT * FROM {} ORDER BY id DESC LIMIT 1"


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
        return user

    def update(self, user: User) -> User:
        self.cursor.execute(UPDATE_USER_QUERY, (user.login, user.password
                                                , user.id,))
        return self.get_by_param(user.id)

    def delete(self, user: User) -> None:
        self.cursor.execute(DELETE_USER_QUERY, (user.login,))

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
            self.cursor.execute(GET_ACCOUNT_BY_ID_QUERY, (item,))
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
        user = user_repository.get_by_param(int(account[3]))
        return Account(id=int(account[0]), name=account[1], description=account[2], user=user,
                       balance=float(account[4]))


class CategoryRepository(ARepository[Category]):

    def create(self, category: Category) -> Category:
        self.cursor.execute(CREATE_CATEGORY_QUERY, (category.name,))
        return self.get_last_row("category")

    def get_by_param(self, item: int | str) -> Category | None:
        if isinstance(item, int):
            self.cursor.execute(GET_CATEGORY_BY_ID_QUERY, (item,))
        elif isinstance(item, str):
            self.cursor.execute(GET_CATEGORY_BY_NAME_QUERY, (item,))
        else:
            logger.error(f"There is no such option for this type")
        result = self.cursor.fetchone()
        category = self.parse(result)
        logger.info(result)
        return category

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


class UserHasCategoryRepository(ARepository[UserCategory]):

    def create(self, user_category: UserCategory) -> bool:
        self.cursor.execute(CREATE_NEW_CATEGORY_QUERY,
                            (user_category.user.id, user_category.category.id))
        return True

    def get_by_param(self, item: User | Category | List) -> List[Category]:
        if isinstance(item, User):
            self.cursor.execute(SELECT_USERS_CATEGORIES_QUERY, (item.id,))
            result = self.cursor.fetchall()
            categories = []
            for category in result:
                categories.append(self.parse(category))
            return categories
        elif isinstance(item, Category):
            self.cursor.execute(SELECT_CATEGORY_COUNT_QUERY, (item.id,))
            return self.cursor.fetchone()
        elif isinstance(item, List):
            self.cursor.execute(
                "select count(*) from user_has_category as u join category as c on u.category_id = c.id where user_id = ? and  c.id =? and c.name =?",
                (item[0].id, item[1].id, item[1].name))
            return self.cursor.fetchone()

        else:
            logger.error(f"There is no such option for this type")

    def update(self, item: T) -> T:
        logger.error(f"There is no such option for this type")
        return None

    def delete(self, user_category: UserCategory) -> None:
        self.cursor.execute(DELETE_USER_HAS_CATEGORY_QUERY,
                            (user_category.user.id, user_category.category.id))

    @staticmethod
    def parse(item_representation: str) -> Category | None:
        return CategoryRepository.parse(item_representation)


class TransactionRepository(ARepository[Transaction]):
    def create(self, transaction: Transaction) -> Transaction:
        if transaction.category is None:
            self.cursor.execute(
                CREATE_TRANSACTION_WITHOUT_CATEGORY_QUERY, (transaction.amount,
                                                            transaction.description,
                                                            transaction.account.id
                                                            ))
        else:
            self.cursor.execute(
                CREATE_TRANSACTION_QUERY, (transaction.amount,
                                           transaction.description,
                                           transaction.account.id,
                                           transaction.category.id
                                           ))
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
                parsed_transaction = self.parse(transaction)
                parsed_transaction.account = item
                transactions.append(parsed_transaction)
            return transactions

    def update(self, transaction: Transaction) -> Transaction:
        self.cursor.execute(UPDATE_TRANSACTION_QUERY, (transaction.amount,
                                                       transaction.description,
                                                       transaction.category.id))
        return self.get_by_param(transaction.id)

    def delete(self, transaction: Transaction) -> None:
        self.cursor.execute(DELETE_TRANSACTION_QUERY, (transaction.id,))

    @staticmethod
    def parse(transaction: str) -> Transaction | None:
        if transaction is None:
            return None

        if not transaction[5]:
            return Transaction(id=int(transaction[0]), account=None, amount=float(transaction[1]),
                               description=transaction[2],
                               date=transaction[3])
        category = Category(id=int(transaction[5]), name=transaction[6])
        return Transaction(id=int(transaction[0]), amount=float(transaction[1]), description=transaction[2],
                           date=transaction[3], account=None, category=category)
