import sys

from PyQt5.QtWidgets import QMainWindow, QApplication, QDialog
from PyQt5.uic import loadUi

from startup import Start
from checklist import Checklist
from genre_language import GenreLang


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("UI\\ui_main.ui", self)
        self.setWindowTitle("Home - Cinematch")


if __name__ == "__main__":

    app = QApplication(sys.argv)
    window = Main()
    start_win = Start()
    checklist_win = Checklist()
    genrelang_win = GenreLang()

    if start_win.exec_() == 1:
        window.show()
    elif start_win.exec_() == 0:
        if checklist_win.exec_() == QDialog.Accepted:
            if genrelang_win.exec_() == QDialog.Accepted:
                window.show()
    else:
        sys.exit(0)

    sys.exit(app.exec_())
