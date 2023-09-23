import sys
from PyQt5.QtCore import pyqtSignal, QObject, QEvent
from PyQt5.QtWidgets import QDialog, QApplication, QStackedWidget, QLineEdit
from PyQt5.uic import loadUi


# Line 156,189,122
# Line 147, modify loginfunction() to check for both email and username

# Line 180 modify the error label shit and all

def clickable(widget):
    """
    Helps to detect the event in which a non-clickable widget (Ex - Label) is clicked by using the Mouse Button Release
    QEvent. A signal is emitted upon clicking the widget on which this function is used. That signal can be relayed to
    the program and the click (mouse release) event can be used.
    :param: widget
    :return: Bool
    """

    class Filter(QObject):

        clicked = pyqtSignal()

        def eventFilter(self, obj, event):

            if obj == widget:
                if event.type() == QEvent.MouseButtonRelease:
                    if obj.rect().contains(event.pos()):
                        self.clicked.emit()
                        return True

            return False

    _filter = Filter(widget)
    widget.installEventFilter(_filter)
    return _filter.clicked


def _reg():
    """Initiates the register function from WelcomeScreen Class"""
    welc = WelcomeScreen()
    welc.register()


def _log():
    """Initiates the login function from WelcomeScreen Class"""
    welc = WelcomeScreen()
    welc.login()


def _for():
    """Initiates the ForgotPassword Class"""
    forgot = ForgotPassword()
    widget.addWidget(forgot)
    widget.setCurrentIndex(widget.currentIndex() + 1)


def _otp():
    """Initiates the OTP Class"""
    otp = OTP()
    widget.addWidget(otp)
    widget.setCurrentIndex(widget.currentIndex() + 1)


def _reset():
    """Initiates the Reset Class"""
    reset = Reset()
    widget.addWidget(reset)
    widget.setCurrentIndex(widget.currentIndex() + 1)


class WelcomeScreen(QDialog):
    def __init__(self):
        super(WelcomeScreen, self).__init__()
        loadUi("Login UI\\startup.ui", self)

        self.register_2.clicked.connect(self.register)
        self.login_2.clicked.connect(self.login)

    def reject(self):
        """Pressing esc key results in the screen going blank cuz this built-in function is called, so we are modifying
         it externally to do nothing when the esc key is pressed."""
        pass

    def login(self):
        login = LoginScreen()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def register(self):
        create = RegisterScreen()
        widget.addWidget(create)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class RegisterScreen(QDialog):
    def __init__(self):
        super(RegisterScreen, self).__init__()
        loadUi("Login UI\\register.ui", self)

        self.passwordfield.setEchoMode(QLineEdit.Password)  # makes the password not visible
        self.confirmpasswordfield.setEchoMode(QLineEdit.Password)
        self._register.clicked.connect(self.registerfunction)

        clickable(self.wanttologin).connect(self.registertologin)

    def reject(self):
        """Pressing esc key results in the screen going blank cuz this built-in function is called, so we are modifying
        it externally to do nothing when the esc key is pressed."""
        pass

    def registertologin(self):
        _log()

    def registerfunction(self):
        user = self.usernamefield.text()
        email = self.emailfield.text()
        password = self.passwordfield.text()
        confirmpassword = self.confirmpasswordfield.text()

        if len(user) == 0 or len(password) == 0 or len(confirmpassword) == 0 or len(email) == 0:
            self.error.setText("Please fill in all inputs.")

        elif len(password) < 8:
            self.error.setText("Password cannot be less than 8 characters.")

        elif len(user) < 3:
            self.error.setText("Username cannot be less than 3 characters.")

        elif password != confirmpassword:
            self.error.setText("Passwords do not match.")

        else:
            print("Registering")
            # Database linkage code
            # Direct to next page (Checklist/Languages)


class LoginScreen(QDialog):
    def __init__(self):
        super(LoginScreen, self).__init__()
        loadUi("Login UI\\login.ui", self)

        self.passwordfield.setEchoMode(QLineEdit.Password)
        self.login.clicked.connect(self.loginfunction)

        clickable(self.wanttoregister).connect(self.logintoregister)
        clickable(self.forgotpswd).connect(self.forgotpassword)

    def reject(self):
        """Pressing esc key results in the screen going blank cuz this built-in function is called, so we are modifying
        it externally to do nothing when the esc key is pressed."""
        pass

    def logintoregister(self):
        _reg()

    def forgotpassword(self):
        _for()

    def loginfunction(self):
        user = self.uidfield.text()
        password = self.passwordfield.text()

        if len(user) == 0 or len(password) == 0:
            self.error.setText("Please fill in all inputs.")

        else:
            print("Logging In")
            # Database linkage code to check credentials
            # check either for username or for email
            # Direct to next page (Splash Screen)


class ForgotPassword(QDialog):
    def __init__(self):
        super(ForgotPassword, self).__init__()
        loadUi("Login UI\\forgot_password.ui", self)
        self.sendmail.clicked.connect(self.sendmailfunction)

        clickable(self.wanttoregister).connect(self.forgottoregister)
        clickable(self.wanttologin).connect(self.forgottologin)

    def reject(self):
        """Pressing esc key results in the screen going blank cuz this built-in function is called, so we are modifying
        it externally to do nothing when the esc key is pressed."""
        pass

    def forgottoregister(self):
        _reg()

    def forgottologin(self):
        _log()

    def sendmailfunction(self):
        email = self.emailfield.text()

        if len(email) == 0:
            self.error.setText("Please fill in all the inputs.")
        else:
            # otp send type shit (preferably separate function so that it can be reused in the send again button in the
            # next window
            _otp()


class OTP(QDialog):
    def __init__(self):
        super(OTP, self).__init__()
        loadUi("Login UI\\otp.ui", self)
        self.checkotp.clicked.connect(self.otpcheck)

        clickable(self.sendagain).connect(self.sendfunc)

    def reject(self):
        """Pressing esc key results in the screen going blank cuz this built-in function is called, so we are modifying
        it externally to do nothing when the esc key is pressed."""
        pass

    def sendfunc(self):
        self.otpfield.setText("")
        print("New Email sent")
        # Reuse the above classes' send mail func code here

    def otpcheck(self):
        otp = self.otpfield.text()

        if len(otp) != 6:
            self.error.setText("The OTP must be 6 characters long.")
            self.success.setText("")

        else:
            # code the otp check function here
            print("OTP transaction done.")
            self.error.setText("")
            self.success.setText("Successful. Redirecting now.")
            _reset()


class Reset(QDialog):
    def __init__(self):
        super(Reset, self).__init__()
        loadUi("Login UI\\resetpswd.ui", self)
        self.newp.setEchoMode(QLineEdit.Password)  # makes the password not visible
        self.confirmnewp.setEchoMode(QLineEdit.Password)
        self.reset.clicked.connect(self.resetfunc)

    def reject(self):
        """Pressing esc key results in the screen going blank cuz this built-in function is called, so we are modifying
        it externally to do nothing when the esc key is pressed."""
        pass

    def resetfunc(self):
        password = self.newp.text()
        confirmpass = self.confirmnewp.text()

        if len(password) == 0 or len(confirmpass) == 0:
            self.error.setText("Passwords cannot be empty.")

        elif password != confirmpass:
            self.error.setText("Passwords do not match.")

        elif len(password) < 8:
            self.error.setText("Password must be at least 8 characters long.")

        else:
            # code to update password in the database
            _log()
            print(widget.currentIndex())


# main
if __name__ == '__main__':
    app = QApplication(sys.argv)
    welcome = WelcomeScreen()

    widget = QStackedWidget()
    widget.addWidget(welcome)
    widget.setFixedWidth(486)
    widget.setFixedHeight(558)
    widget.show()

    sys.exit(app.exec_())
