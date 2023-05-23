class DataValidation:
    @staticmethod
    def is_password_valid(password, second_password):
        if password == second_password:
            return True
        return False