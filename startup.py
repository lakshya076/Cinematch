import sys
import requests
from PyQt5.QtWidgets import QDialog, QApplication, QLineEdit
from PyQt5.uic import loadUi

from reusable_imports.commons import ErrorDialog, clickable
from backend import mailing, users
from reusable_imports.common_vars import conn, cur


def wifi_availability():
    """
    check if the machine is connected to internet or not.
    :return: bool
    """
    try:
        response = requests.get("https://google.com", timeout=4)
        return True
    except requests.ConnectionError:
        return False


class Wifi(ErrorDialog):
    """
    reusable class inherited from ErrorDialog generic class to display a dialog box in the program if
    wi-fi is not connected.
    """

    def __init__(self):
        super(Wifi, self).__init__()

        self.error_dialog.setWindowTitle("Internet Connection Error")
        self.error_dialog.setText("Wifi not connected.\nPlease check your internet connection.")
        self.error_dialog.exec_()


class Start(QDialog):
    def __init__(self):
        super(Start, self).__init__()
        loadUi("UI\\ui_startup.ui", self)
        self.setWindowTitle("Welcome to Cinematch")
        self.stack.setCurrentIndex(0)

        self.register_startup.clicked.connect(self.redirect_register)
        self.login_startup.clicked.connect(self.redirect_login)

        self.pfield_register.setEchoMode(QLineEdit.Password)
        self.cpfield_register.setEchoMode(QLineEdit.Password)
        self.pfield_login.setEchoMode(QLineEdit.Password)
        self.pfield_reset.setEchoMode(QLineEdit.Password)
        self.cpfield_reset.setEchoMode(QLineEdit.Password)

        clickable(self.r_direct_l).connect(self.redirect_login)
        clickable(self.f_direct_l).connect(self.redirect_login)
        clickable(self.l_direct_r).connect(self.redirect_register)
        clickable(self.f_direct_r).connect(self.redirect_register)
        clickable(self.l_direct_f).connect(self.redirect_forgot)
        clickable(self.sendagain).connect(self.send_again)

        self.register_button.clicked.connect(self.directto_reg)
        self.login_button.clicked.connect(self.directto_log)
        self.forgot_button.clicked.connect(self.directto_forgot)
        self.otp_button.clicked.connect(self.directto_otp)
        self.reset_button.clicked.connect(self.directto_reset)

    def directto_reg(self):
        """
        Closes the dialog and sets its result code to 0.
        If this dialog is shown with exec() now, upon clicking the register option, 0 is returned which is then
        used to load checklist (because now the .exec_() function related to this class in the main.py file will
        also return 0).
        Official Documentation -> https://doc.qt.io/qt-5/qdialog.html#done
        """
        # TODO email verification at registration
        user = self.ufield_register.text()
        email = self.efield_register.text()
        password = self.pfield_register.text()
        confirmpassword = self.cpfield_register.text()

        if wifi_availability():
            if len(user) == 0 or len(password) == 0 or len(confirmpassword) == 0 or len(email) == 0:
                self.error_register.setText("Please fill in all inputs.")

            elif len(password) < 8:
                self.error_register.setText("Password cannot be less than 8 characters.")

            elif len(user) < 3:
                self.error_register.setText("Username cannot be less than 3 characters.")

            elif password != confirmpassword:
                self.error_register.setText("Passwords do not match.")

            else:
                # Database linkage code
                if users.register(user, password, email, conn, cur):
                    print("Registering")
                    self.done(1)
                else:
                    self.error_register.setText("Credentials already exists.")

                # Direct to next page (Checklist/Languages)


        else:
            Wifi()

    def directto_log(self):
        """
        Closes the dialog and sets its result code to 1.
        If this dialog is shown with exec() now, upon clicking the register option, 1 is returned which is then
        used to load checklist (because now the .exec_() function related to this class in the main.py file will
        also return 1).
        Official Documentation -> https://doc.qt.io/qt-5/qdialog.html#done
        """

        user = self.ufield_login.text()
        password = self.pfield_login.text()

        if wifi_availability():
            if len(user) == 0 or len(password) == 0:
                self.error_login.setText("Please fill in all inputs.")

            else:
                # Database linkage code to check credentials
                # check either for username or for email

                if users.login(user, password, cur, conn):
                    print("Logging In")
                    self.done(2)
                else:
                    self.error_login.setText("Email/Password combination is incorrect.")
                # Direct to next page (Splash Screen)

        else:
            Wifi()

    def directto_forgot(self):
        self.email = self.efield_forgot.text()

        if wifi_availability():
            if len(self.email) == 0:
                self.error_forgot.setText("Please fill in all the inputs.")
            else:
                # otp send type shit (preferably separate function so that it can be reused in the send again button
                # in next window
                self.sent_otp = mailing.send_otp(self.email)

                self.redirect_otp()
        else:
            Wifi()

    def directto_otp(self):
        otp = self.otp_field.text()

        if wifi_availability():
            if len(otp) != 6:
                self.error_otp.setText("The OTP must be 6 characters long.")
                self.success_otp.setText("")

            else:
                # code the otp check function here
                if otp == str(self.sent_otp):
                    print(otp, self.sent_otp)

                    print("OTP transaction done.")
                    self.error_otp.setText("")
                    self.success_otp.setText("Successful. Redirecting now.")
                    self.redirect_reset()

                else:

                    print("Wrong OTP")
                    self.error_otp.setText("Incorrect OTP")
                    self.success_otp.setText("")

        else:
            Wifi()

    def directto_reset(self):
        password = self.pfield_reset.text()
        confirmpass = self.cpfield_reset.text()

        if wifi_availability():
            if len(password) == 0 or len(confirmpass) == 0:
                self.error_reset.setText("Passwords cannot be empty.")

            elif password != confirmpass:
                self.error_reset.setText("Passwords do not match.")

            elif len(password) < 8:
                self.error_reset.setText("Password must be at least 8 characters long.")

            else:
                # code to update password in the database

                users.update_password(self.email, password, conn, cur)
                self.redirect_login()

        else:
            Wifi()

    def send_again(self):
        if wifi_availability():
            self.otp_field.setText("")
            print("New Email sent")
            # Reuse the send mail func code here

            self.sent_otp = mailing.send_otp(self.email)

        else:
            Wifi()

    def redirect_register(self):
        self.setWindowTitle("Register - Cinematch")
        self.stack.setCurrentIndex(1)
        self.efield_register.setText("")
        self.ufield_register.setText("")
        self.pfield_register.setText("")
        self.cpfield_register.setText("")
        self.error_register.setText("")

    def redirect_login(self):
        self.setWindowTitle("Login - Cinematch")
        self.stack.setCurrentIndex(2)
        self.ufield_login.setText("")
        self.pfield_login.setText("")
        self.error_login.setText("")

    def redirect_forgot(self):
        self.setWindowTitle("Forgot Password - Cinematch")
        self.stack.setCurrentIndex(3)
        self.efield_forgot.setText("")
        self.error_forgot.setText("")

    def redirect_otp(self):
        self.setWindowTitle("OTP - Cinematch")
        self.stack.setCurrentIndex(4)
        self.otp_field.setText("")
        self.error_otp.setText("")
        self.success_otp.setText("")

    def redirect_reset(self):
        self.setWindowTitle("Reset Password - Cinematch")
        self.stack.setCurrentIndex(5)
        self.pfield_reset.setText("")
        self.cpfield_reset.setText("")
        self.error_reset.setText("")

    def reject(self):
        """Pressing esc key results in the screen going blank cuz this built-in function is called, so we are modifying
         it externally to do nothing when the esc key is pressed."""
        pass

    def closeEvent(self, event):
        """
        Although this is not necessary, but after encountering an unknown bug of close button not working in the
        checklist window, we are adding this to prevent bugs related to closing the screen (if exist)
        """
        sys.exit()


# main

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Start()
    window.show()
    sys.exit(app.exec_())
