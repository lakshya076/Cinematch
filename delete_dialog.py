from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi

from backend import users
from reusable_imports.common_vars import cur, conn


class DeleteDialog(QDialog):
    def __init__(self, user: str):
        """
        This dialog is shown when the user tries to delete their account. This dialog asks for the users password and
        if it is correct their account is deleted.
        """
        super(DeleteDialog, self).__init__()
        loadUi("UI\\ui_deletedialog.ui", self)
        self.setWindowTitle("Cinematch - Delete Account")

        self.setModal(False)

        self.user = user

        self.pfield_del.returnPressed.connect(self.pcheck)
        self.del_but.clicked.connect(self.pcheck)

    def pcheck(self) -> None:
        text = self.pfield_del.text()
        pass_ok = users.login(self.user, text, cur, conn)

        if pass_ok:
            self.accept()
        else:
            self.error_label.setText("Password Incorrect")
