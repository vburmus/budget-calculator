import sys
from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow, QWidget
from PyQt5 import QtWidgets
from PyQt5.uic import loadUi
import ui.background_rc


# Login window class
class LoginPage(QWidget):
    def __init__(self):
        super(LoginPage, self).__init__()
        loadUi("ui/LoginPage.ui", self)

        self.signInButton.clicked.connect(self.loginFunction)
        self.createAccButton.clicked.connect(self.gotoSignUpWindow)

    # login function, needs to be connected with logic and database
    def loginFunction(self):
        login = self.loginEnterText.text()
        password = self.passwordEnterText.text()
        if True:
            self.communicateTextLabel.setText("Incorrect password!")
            # widget.setFixedSize()

    def gotoSignUpWindow(self):
        createAccWindow = SignUpPage()
        widget.addWidget(createAccWindow)
        widget.setCurrentIndex(widget.currentIndex() + 1)


# Sign up window class
class SignUpPage(QWidget):
    def __init__(self):
        super(SignUpPage, self).__init__()
        loadUi("ui/SignUpPage.ui", self)
        self.signUpButton.clicked.connect(self.signUpFunction)

    # Sign Up button function -needs to be updated and connected with logic and database
    def signUpFunction(self):
        login = self.loginText.text()
        password = self.passwordText.text()
        confirmPas = self.confirmPasText.text()

        if True:
            self.communicateTextLabel.setText("Incorrect password!")

        else:
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


