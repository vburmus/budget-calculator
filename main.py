import sys

from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5 import QtWidgets
from PyQt5 import uic
import ui.background_rc

from logic.services import *
from loguru import logger


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

        self.signOutButton.clicked.connect(self.sign_out_function)
        self.settingsButton.clicked.connect(self.user_settings)
        self.addAccountButton.clicked.connect(self.goto_adding_new_account)

        self.userName.setText(user.login)

        self.user = user

        self.accountDescription.setText("")
        self.transactionDetails.setText("")

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

        self.communicateTextLabel.setText("")
        self.userNameTextEdit.setText("")
        self.passwordText.setText("")
        self.newPasswordText.setText("")

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

        self.acc_service = AccountService()
        self.user = user

    def exit(self):
        mainWindow = MainPage(self.user)
        widget.addWidget(mainWindow)
        widget.setFixedSize(1325, 788)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def add_new_account(self):
        name = self.AccNameText.text()
        description = self.AccDescrText.text()
        balance = self.AccBalanceText.text()

        # success, message = self.acc_service.create(name, self.user, balance, )


if __name__ == '__main__':
    app = QApplication(sys.argv)
    startWindow = LoginPage()
    widget = QtWidgets.QStackedWidget()
    widget.addWidget(startWindow)
    widget.setFixedSize(549, 626)
    widget.show()
    app.exec_()
