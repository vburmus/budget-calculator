import sys
from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow
from PyQt5 import QtWidgets
from PyQt5.uic import loadUi


# Start window class
class StartWindow(QMainWindow):
    def __init__(self):
        super(StartWindow, self).__init__()
        loadUi("ui/StartWindow.ui", self)

        self.signInButton.clicked.connect(self.loginFunction)
        self.createAccButton.clicked.connect(self.gotoSignUpWindow)
        self.passwordEnterText.setEchoMode(QtWidgets.QLineEdit.Password)

    # login function, needs to be connected with logic and database
    def loginFunction(self):
        login = self.loginEnterText.text()
        password = self.passwordEnterText.text()
        print(f"Logged with login: {login} and password: {password}")  # this print may be deleted in future

    def gotoSignUpWindow(self):
        createAccWindow = CreateAccWindow()
        widget.addWidget(createAccWindow)
        widget.setCurrentIndex(widget.currentIndex() + 1)


# Sign up window class
class CreateAccWindow(QMainWindow):
    def __init__(self):
        super(CreateAccWindow, self).__init__()
        loadUi("ui/CreateAccWindow.ui", self)
        self.signUpButton.clicked.connect(self.signUpFunction)
        self.passwordText.setEchoMode(QtWidgets.QLineEdit.Password)
        self.confirmPasText.setEchoMode(QtWidgets.QLineEdit.Password)

    # Sign Up button function -needs to be updated and connected with logic and database
    def signUpFunction(self):
        # branch to validate confirmation password
        if self.confirmPasText.text() == self.passwordText.text():
            login = self.loginText.text()
            password = self.passwordText.text()
            print(f"Sign up successfully, login: {login}, password: {password}")  # this print may be deleted in future

            # returning to the start window
            startWindow = StartWindow()
            widget.addWidget(startWindow)
            widget.setCurrentIndex(widget.currentIndex() + 1)


if __name__ == '__main__':

    app = QApplication(sys.argv)
    mainWindow = StartWindow()
    widget = QtWidgets.QStackedWidget()
    widget.addWidget(mainWindow)
    widget.setFixedSize(1143, 736)
    widget.show()
    app.exec_()


