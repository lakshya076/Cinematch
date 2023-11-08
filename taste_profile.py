import sys

from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.uic import loadUi

from reusable_imports._css import dark_main_stylesheet, dark_mainwin_widget
from display_movie import DisplayMovies


class TasteProfile(QDialog):
    def __init__(self):
        super(TasteProfile, self).__init__()
        loadUi("UI\\ui_tasteprofile.ui", self)

        self.setModal(False)

        # Setting CSS
        self.setStyleSheet(dark_main_stylesheet)
        self.taste_home.setStyleSheet("background-color:#313a46; border:none;")
        self.taste_search.setStyleSheet("background-color:#313a46; border:none;")

        self.watched.setStyleSheet("font:14pt;")
        self.search.setStyleSheet("font:14pt;")

        self.taste_home.clicked.connect(self.home_func)
        self.taste_search.clicked.connect(self.search_func)

    def home_func(self):
        """
        Function to switch to the home widget in the stack
        """
        self.stack.setCurrentIndex(0)
        if self.expand.isVisible():
            self.expand.hide()
            self.collapse.show()

    def search_func(self):
        """
        Function to switch to the search widget in the stack
        """
        self.stack.setCurrentIndex(1)
        if self.expand.isVisible():
            self.expand.hide()
            self.collapse.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TasteProfile()
    window.show()
    sys.exit(app.exec_())
