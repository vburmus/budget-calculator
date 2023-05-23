import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5 import QtWidgets
from PyQt5.uic import loadUi

from logic.services import UserService
from loguru import logger
import ui.background_rc

# Login window class
class LoginPage(QWidget):
    def __init__(self):
        super(LoginPage, self).__init__()
        loadUi("ui/LoginPage.ui", self)

        self.signInButton.clicked.connect(self.login_function)
        self.createAccButton.clicked.connect(self.goto_sign_up)

        logger.add("logs/application.log", rotation="500 MB", level="INFO")
        self.user_service = UserService()

    # login function, needs to be connected with logic and database
    def login_function(self):
        login = self.loginEnterText.text()
        password = self.passwordEnterText.text()
        success, message = self.user_service.login_user(login, password)

        if not success:
            self.communicateTextLabel.setText(message)
            logger.warning(message)
        else:
            self.communicateTextLabel.setText("")
            # Success login, go t main menu
            logger.success(message)
            # widget.setFixedSize()

    def goto_sign_up(self):
        createAccWindow = SignUpPage()
        widget.addWidget(createAccWindow)
        widget.setCurrentIndex(widget.currentIndex() + 1)


# Sign up window class
class SignUpPage(QWidget):
    def __init__(self):
        super(SignUpPage, self).__init__()
        loadUi("ui/SignUpPage.ui", self)
        self.signUpButton.clicked.connect(self.sign_up_function)

        self.user_service = UserService()

    # Sign Up button function -needs to be updated and connected with logic and database
    def sign_up_function(self):
        login = self.loginText.text()
        password = self.passwordText.text()
        confirm_password = self.confirmPasText.text()

        success, message = self.user_service.register_user(login, password, confirm_password)

        if not success:
            self.communicateTextLabel.setText(message)
            logger.warning(message)
        else:
            self.communicateTextLabel.setText("")
            # Success login, go t main menu
            logger.success(message)
            # returning to the start window
            loginWindow = LoginPage()
            widget.addWidget(loginWindow)
            widget.setCurrentIndex(widget.currentIndex() + 1)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    startWindow = LoginPage()
    widget = QtWidgets.QStackedWidget()
    widget.addWidget(startWindow)
    widget.setFixedSize(549, 626)
    widget.show()
    app.exec_()
