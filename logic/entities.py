class User:
    def __init__(self, id: int = None, login: str = None, password: str = None, balance: float = None) -> object:
        self._id = id
        self._login = login
        self._password = password
        self._balance = balance

    @property
    def id(self):
        return self._id

    @property
    def login(self):
        return self._login

    @property
    def password(self):
        return self._password

    @property
    def balance(self):
        return self._balance
