import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.uic import loadUi

from reusable_imports._css import dark_main_stylesheet, dark_mainwin_widget


class TasteProfile(QDialog):
    def __init__(self):
        super(TasteProfile, self).__init__()
        loadUi("UI\\ui_tasteprofile.ui", self)

        self.setModal(False)

        # Setting CSS
        self.setStyleSheet(dark_main_stylesheet)
        self.taste_home.setStyleSheet("background-color:#313a46; border:none;")
        self.taste_search.setStyleSheet("background-color:#313a46; border:none;")

        self.watched.setStyleSheet(dark_mainwin_widget)
        self.search.setStyleSheet(dark_mainwin_widget)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TasteProfile()
    window.show()
    sys.exit(app.exec_())
