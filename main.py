import sys

from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QListWidget, QListWidgetItem
from PyQt5 import QtWidgets
from PyQt5 import uic
import ui.background_rc

from logic.services import *
from loguru import logger


# goto pages methods
def goto_sign_up():
    createAccWindow = SignUpPage()
    widget.addWidget(createAccWindow)
    widget.setCurrentIndex(widget.currentIndex() + 1)


def goto_main_page(user):
    mainWindow = MainPage(user)
    widget.addWidget(mainWindow)
    widget.setFixedSize(1325, 789)
    widget.setCurrentIndex(widget.currentIndex() + 1)


def goto_login_page():
    loginWindow = LoginPage()
    widget.addWidget(loginWindow)
    widget.setFixedSize(1325, 789)
    widget.setCurrentIndex(widget.currentIndex() + 1)


def goto_user_settings(user):
    userPage = UserSettingsPage(user)
    widget.addWidget(userPage)
    widget.setFixedSize(1325, 789)
    widget.setCurrentIndex(widget.currentIndex() + 1)


def goto_adding_new_account(user):
    addAcc = AddAccountPage(user)
    widget.addWidget(addAcc)
    widget.setFixedSize(1325, 789)
    widget.setCurrentIndex(widget.currentIndex() + 1)


def goto_manage_account_page(current_account, user):
    if current_account:
        manageAcc = ManageAccountPage(user, current_account)
        widget.addWidget(manageAcc)
        widget.setFixedSize(1325, 789)
        widget.setCurrentIndex(widget.currentIndex() + 1)


def goto_change_transaction_page(user, account):
    changeTrans = ChangeTransactionPage(user, account)
    widget.addWidget(changeTrans)
    widget.setFixedSize(1325, 789)
    widget.setCurrentIndex(widget.currentIndex() + 1)


def goto_add_transaction_page(user, current_account):
    addTrans = AddTransactionPage(user, current_account)
    widget.addWidget(addTrans)
    widget.setFixedSize(1325, 789)
    widget.setCurrentIndex(widget.currentIndex() + 1)


def goto_manage_categories_page(user):
    manageCat = ManageCategoriesPage(user)
    widget.addWidget(manageCat)
    widget.setFixedSize(1325, 789)
    widget.setCurrentIndex(widget.currentIndex() + 1)


def goto_add_category_page(user):
    addCat = AddCategoryPage(user)
    widget.addWidget(addCat)
    widget.setFixedSize(1325, 789)
    widget.setCurrentIndex(widget.currentIndex() + 1)


class ApplicationService:
    @staticmethod
    def clear_fields(list_of_lines: List[QLineEdit]):
        for elem in list_of_lines:
            elem.setText("")


# Login window class
class LoginPage(QWidget):
    def __init__(self):
        super(LoginPage, self).__init__()
        uic.loadUi("ui/LoginPage.ui", self)

        self.signInButton.clicked.connect(self.login_function)
        self.createAccButton.clicked.connect(goto_sign_up)

        logger.add("logs/application.log", rotation="500 MB", level="INFO")
        self.user_service = UserService()

    def login_function(self):
        success, message = self.user_service.login(self.loginEnterText.text(), self.passwordEnterText.text())

        if not success:
            self.communicateTextLabel.setText(message)
            logger.warning(message)
        else:
            self.communicateTextLabel.setText("")
            logger.success(message)

            goto_main_page(success)


# Sign up window class
class SignUpPage(QWidget):
    def __init__(self):
        super(SignUpPage, self).__init__()
        uic.loadUi("ui/SignUpPage.ui", self)

        self.signUpButton.clicked.connect(self.sign_up_function)
        self.exitButton.clicked.connect(goto_login_page)

        self.user_service = UserService()

    def sign_up_function(self):
        success, message = self.user_service.register(self.loginText.text(),
                                                      self.passwordText.text(),
                                                      self.confirmPasText.text())
        if not success:
            self.communicateTextLabel.setText(message)
            logger.warning(message)
        else:
            self.communicateTextLabel.setText("")
            logger.success(message)
            goto_login_page()


class MainPage(QWidget):
    def __init__(self, user):
        super(MainPage, self).__init__()
        uic.loadUi("ui/MainPage.ui", self)

        self.account_service = AccountService()
        self.user_service = UserService()
        self.user = user

        self.accountDescription.setText("")
        self.transactionDetails.setText("")
        self.userName.setText(self.user.login)

        self.signOutButton.clicked.connect(goto_login_page)
        self.settingsButton.clicked.connect(lambda: goto_user_settings(self.user))
        self.addAccountButton.clicked.connect(lambda: goto_adding_new_account(self.user))
        self.manageAccButton.clicked.connect(lambda: goto_manage_account_page(self.current_account, self.user))
        self.manageCatButton.clicked.connect(lambda: goto_manage_categories_page(self.user))
        self.addTransactionButton.clicked.connect(lambda: goto_add_transaction_page(self.user, self.current_account))
        self.changeTransactionButton.clicked.connect(lambda: goto_change_transaction_page(self.user,
                                                                                          self.current_account))
        # self.deleteTransButton.clicked.connect(self.delete_transaction)

        self.transactionsListBox.itemSelectionChanged.connect(self.transaction_chosen)

        self.comboBoxAccounts.currentTextChanged.connect(self.account_changed)

        # TODO add transactions of the account

        self.current_account = None
        self.loading_user_accounts(self.account_service.get_user_accounts(self.user))

        if self.current_account:
            self.current_transaction = None
            self.account_transactions = self.account_service.get_account_transactions(self.current_account)
            self.current_transaction_index = -1
            self.refresh_transactions()

    def loading_user_accounts(self, user_accounts):
        if len(user_accounts) != 0:
            for account in user_accounts:
                self.comboBoxAccounts.addItem(account.name)
            self.account_changed()

    def refresh_transactions(self):
        self.transactionsListBox.clear()
        self.transactionDetails.setText("")
        self.account_transactions = self.account_service.get_account_transactions(self.current_account)
        for transaction in self.account_transactions:
            # TODO change transaction representation
            self.transactionsListBox.addItem(TransactionDetailsService.to_string_short(transaction))
        self.current_transaction = None

    # TODO add transactions of the account
    def account_changed(self):
        logger.info(f"Changed account to {self.comboBoxAccounts.currentText()}")

        user_accounts = self.account_service.get_user_accounts(self.user)

        self.current_account = user_accounts[self.comboBoxAccounts.currentIndex()]
        self.accountDescription.setText(self.current_account.description)
        self.accountBalanceLabel.setText("Your account balance: " + str(self.current_account.balance))
        self.refresh_transactions()

    def transaction_chosen(self):
        selected_items = self.transactionsListBox.selectedItems()
        if not selected_items:
            return
        selected_item = selected_items[0]

        self.current_transaction = self.account_transactions[self.transactionsListBox.row(selected_item)]

        self.transactionDetails.setText(TransactionDetailsService.to_string_long(self.current_transaction))


class UserSettingsPage(QWidget):
    def __init__(self, user):
        super(UserSettingsPage, self).__init__()
        uic.loadUi("ui/UserSettingsPage.ui", self)

        self.user_service = UserService()
        self.user = user

        self.exitButton.clicked.connect(lambda: goto_main_page(self.user))
        self.submitButton.clicked.connect(self.submit_changes)
        self.deleteAccountButton.clicked.connect(self.delete_account)

        self.communicateTextLabel.setText("")
        self.refresh_username_labels(user)

    def delete_account(self):
        success, message = self.user_service.delete(self.user, self.passwordText.text())
        if success:
            goto_login_page()
        else:
            self.communicateTextLabel.setText(message)
            self.passwordText.setText("")

    def refresh_username_labels(self, user):
        self.userName.setText(user.login)
        self.userNameTextEdit.setPlaceholderText(user.login)

    def submit_changes(self):
        success, response = self.user_service.update(self.user, self.passwordText.text(),
                                                     self.userNameTextEdit.text(), self.newPasswordText.text())

        ApplicationService.clear_fields([self.communicateTextLabel, self.userNameTextEdit,
                                         self.passwordText, self.newPasswordText])

        if success:
            self.user = response
            self.refresh_username_labels(self.user)
        else:
            self.communicateTextLabel.setText(response)


class AddAccountPage(QWidget):
    def __init__(self, user):
        super(AddAccountPage, self).__init__()
        uic.loadUi("ui/AddAccountPage.ui", self)

        self.account_service = AccountService()
        self.user = user

        self.exitButton.clicked.connect(lambda: goto_main_page(self.user))
        self.addButton.clicked.connect(self.add_new_account)

        self.communicateTextLabel.setText("")

    def add_new_account(self):
        success, message = self.account_service.create(self.AccNameText.text(), self.user,
                                                       self.AccBalanceText.text(), self.AccDescrText.text())

        ApplicationService.clear_fields([self.AccNameText, self.AccDescrText,
                                         self.AccBalanceText, self.communicateTextLabel])

        if not success:
            self.communicateTextLabel.setStyleSheet("color: rgb(255, 112, 114);")
            self.communicateTextLabel.setText(message)
        else:
            self.communicateTextLabel.setStyleSheet("color:  rgb(170, 255, 127);")
            self.communicateTextLabel.setText("Account added!")


class ManageAccountPage(QWidget):
    def __init__(self, user, account):
        super(ManageAccountPage, self).__init__()
        uic.loadUi("ui/ManageAccountPage.ui", self)

        self.user = user
        self.account = account
        self.account_service = AccountService()

        self.communicateTextLabel.setText("")
        self.change_text_fields()

        self.submitButton.clicked.connect(self.submit_changes)
        self.exitButton.clicked.connect(lambda: goto_main_page(self.user))
        self.deleteAccountButton.clicked.connect(self.delete_current_account)

    def change_text_fields(self):
        self.AccNameText.setPlaceholderText(self.account.name)
        self.AccBalanceText.setPlaceholderText(str(self.account.balance))

    def submit_changes(self):
        success, message_or_account = self.account_service.update(self.account, self.AccNameText.text(),
                                                                  self.AccDescrText.text(),
                                                                  self.AccBalanceText.text())
        if not success:
            self.communicateTextLabel.setStyleSheet("color: rgb(255, 112, 114);")
            self.communicateTextLabel.setText(message_or_account)
        else:
            self.communicateTextLabel.setStyleSheet("color:  rgb(170, 255, 127);")
            self.communicateTextLabel.setText("Account changed!")
            self.account = message_or_account
            self.change_text_fields()
        ApplicationService.clear_fields([self.AccNameText, self.AccBalanceText, self.AccDescrText])

    def delete_current_account(self):
        if self.account:
            success, message = self.account_service.delete(self.account)
            if success:
                logger.info(message)
            else:
                logger.warning(message)
            goto_main_page(self.user)


class ManageCategoriesPage(QWidget):
    def __init__(self, user):
        super(ManageCategoriesPage, self).__init__()
        uic.loadUi("ui/ManageCategoriesPage.ui", self)

        self.user = user
        self.user_service = UserService()
        self.category_service = CategoryService()
        self.current_category = None

        self.exitButton.clicked.connect(lambda: goto_main_page(self.user))
        self.addCatButton.clicked.connect(lambda: goto_add_category_page(self.user))
        self.deleteCategoryButton.clicked.connect(self.delete_category)
        self.submitButton.clicked.connect(self.update_category)

        self.categoriesListBox.itemSelectionChanged.connect(self.category_chose)

        self.CategoryNameText.setPlaceholderText("")
        self.communicateTextLabel.setText("")

        self.refresh_categories()

    # TODO stylesheet
    def category_chose(self):
        selected_items = self.categoriesListBox.selectedItems()
        if not selected_items:
            return
        selected_item = selected_items[0]
        self.current_category = self.category_service.get_category_by_name(selected_item.text())

        self.CategoryNameText.setPlaceholderText(self.current_category.name)
        self.communicateTextLabel.setText("")

    def refresh_categories(self):
        self.categoriesListBox.clear()
        self.CategoryNameText.setPlaceholderText("")
        for category in self.user_service.get_user_categories(self.user):
            self.categoriesListBox.addItem(category.name)
        self.current_category = None

    def delete_category(self):
        if self.current_category:
            self.user_service.delete_category_from_user(self.user, self.current_category)
            self.refresh_categories()
        else:
            self.communicateTextLabel.setText("Choose the category")

    def update_category(self):
        if self.current_category:
            success, message = self.category_service.update(self.current_category, self.CategoryNameText.text())

            if success:
                self.refresh_categories()
                self.communicateTextLabel.setText("")
            else:
                self.communicateTextLabel.setText(message)
                logger.warning(message)

            ApplicationService.clear_fields([self.CategoryNameText])


class AddCategoryPage(QWidget):
    def __init__(self, user):
        super(AddCategoryPage, self).__init__()
        uic.loadUi("ui/AddCategoryPage.ui", self)

        self.user = user
        self.user_service = UserService()

        self.exitButton.clicked.connect(lambda: goto_manage_categories_page(self.user))
        self.addButton.clicked.connect(self.add_category)

        self.communicateTextLabel.setText("")

    def add_category(self):
        success, message = self.user_service.add_category_user(self.user, self.CategoryNameText.text())

        if success:
            self.communicateTextLabel.setStyleSheet("color:  rgb(170, 255, 127);")
            self.communicateTextLabel.setText("Category added!")
        else:
            self.communicateTextLabel.setStyleSheet("color: rgb(255, 112, 114);")
            self.communicateTextLabel.setText(message)

        ApplicationService.clear_fields([self.CategoryNameText])


class AddTransactionPage(QWidget):
    def __init__(self, user, account):
        super(AddTransactionPage, self).__init__()
        uic.loadUi("ui/AddTransactionPage.ui", self)

        self.user_service = UserService()
        self.account_service = AccountService()
        self.user = user
        self.account = account
        self.current_category = None

        self.communicateTextLabel.setText("")

        self.exitButton.clicked.connect(lambda: goto_main_page(self.user))
        self.addTransButton.clicked.connect(self.add_transaction)

        self.categoriesComboBox.currentTextChanged.connect(self.category_changed)

        self.update_categories(self.user_service.get_user_categories(self.user))

    def update_categories(self, user_categories):
        if len(user_categories) != 0:
            for category in user_categories:
                self.categoriesComboBox.addItem(category.name)
            self.category_changed()

    def category_changed(self):
        logger.info(f"Changed category to {self.categoriesComboBox.currentText()}")

        self.current_category = self.user_service.get_user_categories(self.user)[self.categoriesComboBox.currentIndex()]

    def add_transaction(self):
        success, message = self.account_service.create_transaction(self.AmountText.text(), self.TransDescrText.text(),
                                                                   self.account, self.current_category)

        if success:
            self.communicateTextLabel.setStyleSheet("color:  rgb(170, 255, 127);")
            self.communicateTextLabel.setText("Transaction added!")
        else:
            self.communicateTextLabel.setStyleSheet("color: rgb(255, 112, 114);")
            self.communicateTextLabel.setText(message)
        ApplicationService.clear_fields([self.AmountText, self.TransDescrText])


class ChangeTransactionPage(QWidget):
    def __init__(self, user, account):
        super(ChangeTransactionPage, self).__init__()
        uic.loadUi("ui/ChangeTransactionPage.ui", self)

        self.user_service = UserService()
        self.user = user
        self.current_category = None

        self.exitButton.clicked.connect(lambda: goto_main_page(self.user))
        self.submitButton.clicked.connect(self.submit_changes)

        self.categoriesComboBox.currentTextChanged.connect(self.category_changed)

        self.update_categories(self.user_service.get_user_categories(self.user))

    def update_categories(self, user_categories):
        if len(user_categories) != 0:
            for category in user_categories:
                self.categoriesComboBox.addItem(category.name)
            self.category_changed()

    def category_changed(self):
        logger.info(f"Changed category to {self.categoriesComboBox.currentText()}")

        user_categories = self.user_service.get_user_categories(self.user)

        self.current_category = user_categories[self.categoriesComboBox.currentIndex()]

    def submit_changes(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    startWindow = LoginPage()
    widget = QtWidgets.QStackedWidget()
    widget.addWidget(startWindow)
    widget.setFixedSize(1325, 789)
    widget.show()
    app.exec_()
