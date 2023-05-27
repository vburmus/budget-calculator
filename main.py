import sys

from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit
from PyQt5 import QtWidgets
from PyQt5 import uic
import ui.background_rc

from logic.services import *
from loguru import logger

class ApplicationService():
    @staticmethod
    def clear_fields(list_of_lines:List[QLineEdit]):
        for elem in list_of_lines:
            elem.setText("")


# Login window class
class LoginPage(QWidget):
    def __init__(self):
        super(LoginPage, self).__init__()
        uic.loadUi("ui/LoginPage.ui", self)

        self.signInButton.clicked.connect(self.login_function)
        self.createAccButton.clicked.connect(self.goto_sign_up)

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
            mainWindow = MainPage(success)
            widget.addWidget(mainWindow)
            widget.setFixedSize(1325, 788)
            widget.setCurrentIndex(widget.currentIndex() + 1)

    def goto_sign_up(self):
        createAccWindow = SignUpPage()
        widget.addWidget(createAccWindow)
        widget.setCurrentIndex(widget.currentIndex() + 1)


# Sign up window class
class SignUpPage(QWidget):
    def __init__(self):
        super(SignUpPage, self).__init__()
        uic.loadUi("ui/SignUpPage.ui", self)

        self.signUpButton.clicked.connect(self.sign_up_function)
        self.exitButton.clicked.connect(self.return_to_login_page)

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
            # returning to the start window
            loginWindow = LoginPage()
            widget.addWidget(loginWindow)
            widget.setCurrentIndex(widget.currentIndex() + 1)

    def return_to_login_page(self):
        loginWindow = LoginPage()
        widget.addWidget(loginWindow)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class MainPage(QWidget):
    def __init__(self, user):
        super(MainPage, self).__init__()
        uic.loadUi("ui/MainPage.ui", self)

        self.accountDescription.setText("")
        self.transactionDetails.setText("")

        self.signOutButton.clicked.connect(self.sign_out_function)
        self.settingsButton.clicked.connect(self.user_settings)
        self.addAccountButton.clicked.connect(self.goto_adding_new_account)

        self.account_service = AccountService()
        self.user = user

        self.userName.setText(self.user.login)

        # TODO add transactions of the account
        user_accounts = self.account_service.get_user_accounts(self.user)

        self.current_account = None

        if len(user_accounts) != 0:
            for account in user_accounts:
                self.comboBoxAccounts.addItem(account.name)
            self.account_changed()

        self.comboBoxAccounts.currentTextChanged.connect(self.account_changed)

    # TODO add transactions of the account
    def account_changed(self):
        logger.info(f"Changed account to {self.comboBoxAccounts.currentText()}")

        user_accounts = self.account_service.get_user_accounts(self.user)

        self.current_account = user_accounts[self.comboBoxAccounts.currentIndex()]
        self.accountDescription.setText(self.current_account.description)
        self.accountBalanceLabel.setText("Your account balance: " + str(self.current_account.balance))



    def sign_out_function(self):
        loginWindow = LoginPage()
        widget.addWidget(loginWindow)
        widget.setFixedSize(549, 626)
        widget.setCurrentIndex(widget.currentIndex() + 1)
        self.user = None

    def user_settings(self):
        userPage = UserSettingsPage(self.user)
        widget.addWidget(userPage)
        widget.setFixedSize(538, 768)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def goto_adding_new_account(self):
        addAcc = AddAccountPage(self.user)
        widget.addWidget(addAcc)
        widget.setFixedSize(538, 768)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class UserSettingsPage(QWidget):
    def __init__(self, user):
        super(UserSettingsPage, self).__init__()
        uic.loadUi("ui/UserSettingsPage.ui", self)

        self.exitButton.clicked.connect(self.exit)
        self.submitButton.clicked.connect(self.submit_changes)
        self.deleteAccountButton.clicked.connect(self.delete_account)

        self.communicateTextLabel.setText("")
        self.refresh_username_labels(user)

        self.user_service = UserService()
        self.user = user

    def delete_account(self):
        success, message = self.user_service.delete(self.user, self.passwordText.text())
        if success:
            loginWindow = LoginPage()
            widget.addWidget(loginWindow)
            widget.setFixedSize(549, 626)
            widget.setCurrentIndex(widget.currentIndex() + 1)
        else:
            self.communicateTextLabel.setText(message)
            self.passwordText.setText("")

    def refresh_username_labels(self, user):
        self.userName.setText(user.login)
        self.userNameTextEdit.setPlaceholderText(user.login)

    def exit(self):
        mainWindow = MainPage(self.user)
        widget.addWidget(mainWindow)
        widget.setFixedSize(1325, 788)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def submit_changes(self):
        success, response = self.user_service.update(self.user, self.passwordText.text(),
                                                     self.userNameTextEdit.text(), self.newPasswordText.text())

        ApplicationService.clear_fields([self.communicateTextLabel,self.userNameTextEdit,
                                         self.passwordText,self.newPasswordText])

        if success:
            self.user = response
            self.refresh_username_labels(self.user)
        else:
            self.communicateTextLabel.setText(response)


class AddAccountPage(QWidget):
    def __init__(self, user):
        super(AddAccountPage, self).__init__()
        uic.loadUi("ui/AddAccountPage.ui", self)

        self.exitButton.clicked.connect(self.exit)
        self.addButton.clicked.connect(self.add_new_account)

        self.communicateTextLabel.setText("")

        self.account_service = AccountService()
        self.user = user

    def exit(self):
        mainWindow = MainPage(self.user)
        widget.addWidget(mainWindow)
        widget.setFixedSize(1325, 788)
        widget.setCurrentIndex(widget.currentIndex() + 1)

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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    startWindow = LoginPage()
    widget = QtWidgets.QStackedWidget()
    widget.addWidget(startWindow)
    widget.setFixedSize(549, 626)
    widget.show()
    app.exec_()
