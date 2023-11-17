import re
import sys
import requests
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QApplication, QLineEdit
from PyQt5.uic import loadUi

from reusable_imports.commons import ErrorDialog, clickable
from backend import mailing, users
from reusable_imports.common_vars import conn, cur
from backend.Utils import user_utils

error_css = "border: 2px solid red;font:14pt;border-radius:10px;padding:2 10px;"
mail_reg = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
user_reg = r'^[a-zA-Z_.]{3,}$'
pass_reg = r"^[A-Za-z0-9!@#$%^&*()_+-={}:\";',./<>?|\[\]]{8,20}"


def wifi_availability() -> bool:
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
    """
    This window is shown when the user is either logged out or is using Cinematch for the first time.
    Also supports user verification during registration, resetting password and forgot password.
    """

    def __init__(self):
        super(Start, self).__init__()
        loadUi("UI\\ui_startup.ui", self)
        self.setWindowTitle("Welcome to Cinematch")
        self.setWindowIcon(QIcon("Icons/logo.png"))
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

        # Signal/Slotting
        self.register_button.clicked.connect(self.directto_reg)
        self.login_button.clicked.connect(self.directto_log)
        self.forgot_button.clicked.connect(self.directto_forgot)
        self.otp_button.clicked.connect(self.directto_otp)
        self.reset_button.clicked.connect(self.directto_reset)

        self.efield_register.returnPressed.connect(self.register_enter_check)
        self.ufield_register.returnPressed.connect(self.register_enter_check)
        self.pfield_register.returnPressed.connect(self.register_enter_check)
        self.cpfield_register.returnPressed.connect(self.register_enter_check)

        self.ufield_login.returnPressed.connect(self.login_enter_check)
        self.pfield_login.returnPressed.connect(self.login_enter_check)

        self.efield_forgot.returnPressed.connect(self.forgot_enter_check)

        self.otp_field.returnPressed.connect(self.otp_enter_check)

        self.pfield_reset.returnPressed.connect(self.reset_enter_check)
        self.cpfield_reset.returnPressed.connect(self.reset_enter_check)

    def directto_reg(self):
        """
        Closes the dialog and sets its result code to 0.
        If this dialog is shown with exec() now, upon clicking the register option, 0 is returned which is then
        used to load checklist (because now the .exec_() function related to this class in the main.py file will
        also return 0).
        Official Documentation -> https://doc.qt.io/qt-5/qdialog.html#done
        """
        self.css_reset()
        user = self.ufield_register.text()
        email = self.efield_register.text()
        password = self.pfield_register.text()
        confirmpassword = self.cpfield_register.text()
        name_stat = user_utils.user_status(user, cur)
        mail_stat = user_utils.user_status(email, cur)

        if wifi_availability():
            if len(user) == 0 or len(password) == 0 or len(confirmpassword) == 0 or len(email) == 0:
                self.error_register.setText("Please fill in all inputs.")

            elif len(password) < 8:
                self.error_register.setText("Password cannot be less than 8 characters.")
                self.pfield_register.setStyleSheet(error_css)
                self.cpfield_register.setStyleSheet(error_css)

            elif password != confirmpassword:
                self.error_register.setText("Passwords do not match.")
                self.pfield_register.setStyleSheet(error_css)
                self.cpfield_register.setStyleSheet(error_css)

            elif not re.fullmatch(pass_reg, password):
                self.error_register.setText("Enter a valid password.")
                self.pfield_register.setStyleSheet(error_css)
                self.cpfield_register.setStyleSheet(error_css)

            elif not re.fullmatch(mail_reg, email):
                self.error_register.setText("Enter a valid email address.")
                self.efield_register.setStyleSheet(error_css)

            elif not re.fullmatch(user_reg, user):
                self.error_register.setText("Enter a valid username.\nMake sure its not less than 3 characters.")
                self.ufield_register.setStyleSheet(error_css)

            elif name_stat != 0 or mail_stat != 0:
                if name_stat == 1 or mail_stat == 1:
                    self.error_register.setText("Credentials already exist.")
                elif name_stat == 2 or mail_stat == 2:
                    self.error_register.setText("User is deleted. Recovery available.")

            else:
                self.email = email
                self.username = user
                self.password = password
                self.sent_otp = mailing.send_otp(self.email)
                self.reg = 1
                self.redirect_otp()

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
        self.css_reset()
        user = self.ufield_login.text()
        password = self.pfield_login.text()

        if wifi_availability():
            if len(user) == 0:
                self.error_login.setText("Please fill in all inputs.")
                self.ufield_login.setStyleSheet(error_css)

            elif len(password) == 0:
                self.error_login.setText("Please fill in all inputs")
                self.pfield_login.setStyleSheet(error_css)

            else:
                if users.login(user, password, cur, conn):
                    print("Logging In")
                    self.done(2)
                    # Splash Screen Redirect
                else:
                    self.error_login.setText("Email/Password combination is incorrect.")
                    self.ufield_login.setStyleSheet(error_css)
                    self.pfield_login.setStyleSheet(error_css)
        else:
            Wifi()

    def directto_forgot(self):
        self.css_reset()

        email = self.efield_forgot.text()

        if wifi_availability():
            status = user_utils.user_status(email, cur)

            if len(email) == 0:
                self.error_forgot.setText("Please fill in all the inputs.")
                self.efield_forgot.setStyleSheet(error_css)

            elif status == 0:
                self.error_forgot.setText("This user doesn't exist")
                self.efield_forgot.setStyleSheet(error_css)

            elif status == 2:
                self.error_forgot.setText("This user has been deleted.")
                self.efield_forgot.setStyleSheet(error_css)

            else:
                self.email = email
                self.sent_otp = mailing.send_otp(self.email)
                self.reg = 0
                self.redirect_otp()
        else:
            Wifi()

    def directto_otp(self):
        self.css_reset()
        otp = self.otp_field.text()

        if wifi_availability():
            if len(otp) != 6:
                self.error_otp.setText("The OTP must be 6 characters long.")
                self.success_otp.setText("")
                self.otp_field.setStyleSheet(error_css)

            else:
                if otp == str(self.sent_otp):
                    print(otp, self.sent_otp)

                    print("OTP transaction done.")
                    self.error_otp.setText("")
                    self.success_otp.setText("Successful. Redirecting now.")

                    if self.reg:
                        self.done(1)
                    else:
                        self.redirect_reset()

                else:
                    print("Wrong OTP")
                    self.error_otp.setText("Incorrect OTP")
                    self.success_otp.setText("")
                    self.otp_field.setStyleSheet(error_css)

        else:
            Wifi()

    def directto_reset(self):
        self.css_reset()
        password = self.pfield_reset.text()
        confirmpass = self.cpfield_reset.text()

        if wifi_availability():
            if len(password) == 0 or len(confirmpass) == 0:
                self.error_reset.setText("Passwords cannot be empty.")
                self.pfield_reset.setStyleSheet(error_css)
                self.cpfield_reset.setStyleSheet(error_css)

            elif password != confirmpass:
                self.error_reset.setText("Passwords do not match.")
                self.pfield_reset.setStyleSheet(error_css)
                self.cpfield_reset.setStyleSheet(error_css)

            elif len(password) < 8:
                self.error_reset.setText("Password must be at least 8 characters long.")
                self.pfield_reset.setStyleSheet(error_css)
                self.cpfield_reset.setStyleSheet(error_css)

            else:
                users.update_password(self.email, password, conn, cur)  # Passwords updated in db
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
        self.efield_register.setText("")
        self.ufield_register.setText("")
        self.pfield_register.setText("")
        self.cpfield_register.setText("")
        self.error_register.setText("")
        self.css_reset()
        self.stack.setCurrentIndex(1)

    def redirect_login(self):
        self.setWindowTitle("Login - Cinematch")
        self.ufield_login.setText("")
        self.pfield_login.setText("")
        self.error_login.setText("")
        self.css_reset()
        self.stack.setCurrentIndex(2)

    def redirect_forgot(self):
        self.setWindowTitle("Forgot Password - Cinematch")
        self.efield_forgot.setText("")
        self.error_forgot.setText("")
        self.css_reset()
        self.stack.setCurrentIndex(3)

    def redirect_otp(self):
        self.setWindowTitle("OTP - Cinematch")
        self.otp_field.setText("")
        self.error_otp.setText("")
        self.success_otp.setText("")
        self.css_reset()
        self.stack.setCurrentIndex(4)

    def redirect_reset(self):
        self.setWindowTitle("Reset Password - Cinematch")
        self.pfield_reset.setText("")
        self.cpfield_reset.setText("")
        self.error_reset.setText("")
        self.css_reset()
        self.stack.setCurrentIndex(5)

    def css_reset(self):
        text_box = """
        background-color:rgba(0,0,0,0);
        font: 14pt;
        background:#FFFAF0;
        selection-background-color: black;
        border-width: 1px; 
        border-style: solid; border-color: black black black black; border-radius: 10px;padding: 2 10px;"""

        self.efield_register.setStyleSheet(text_box)
        self.ufield_register.setStyleSheet(text_box)
        self.pfield_register.setStyleSheet(text_box)
        self.cpfield_register.setStyleSheet(text_box)
        self.ufield_login.setStyleSheet(text_box)
        self.pfield_login.setStyleSheet(text_box)
        self.efield_forgot.setStyleSheet(text_box)
        self.otp_field.setStyleSheet(text_box)
        self.pfield_reset.setStyleSheet(text_box)
        self.cpfield_reset.setStyleSheet(text_box)

    def register_enter_check(self):
        if not (not (self.efield_register.text() != "") or not (self.ufield_register.text() != "") or not (
                self.pfield_register.text() != "") or not (self.cpfield_register.text() != "")):
            self.directto_reg()
        else:
            self.error_register.setText("Please fill in all the details.")

    def login_enter_check(self):
        if not (not (self.ufield_login.text() != "") or not (self.pfield_login.text() != "")):
            self.directto_log()
        else:
            self.error_login.setText("Please fill in all the details.")

    def forgot_enter_check(self):
        if self.efield_forgot.text() != "":
            self.directto_forgot()
        else:
            self.error_login.setText("Please fill in all the details.")
            self.efield_forgot.setStyleSheet(error_css)

    def otp_enter_check(self):
        if self.otp_field.text() != "":
            self.directto_otp()
        else:
            self.error_login.setText("Please fill in all the details.")
            self.otp_field.setStyleSheet(error_css)

    def reset_enter_check(self):
        if self.pfield_reset.text() != "" and self.cpfield_reset.text() != "":
            self.directto_reset()
        else:
            self.error_login.setText("Please fill in all the details.")
            self.pfield_reset.setStyleSheet(error_css)
            self.cpfield_reset.setStyleSheet(error_css)

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
