import hashlib


class DataValidation:
    @staticmethod
    def is_passwords_are_same(password, second_password):
        if password == second_password:
            return True
        return False

    @staticmethod
    def is_password_valid(db_password, password):
        if DataValidation.encode_password(password) == db_password:
            return True
        return False

    @staticmethod
    def encode_password(password):
        hash_algorithm = hashlib.sha256()
        hash_algorithm.update(password.encode('utf-8'))
        encoded_password = hash_algorithm.hexdigest()
        return encoded_password
