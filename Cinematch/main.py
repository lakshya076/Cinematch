import os.path
import sys
import ctypes

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QApplication, QDialog, QMessageBox, QPushButton
from PyQt5.uic import loadUi

from startup import Start
from checklist import Checklist
from genre import Genre
from language import Language

from reusable_imports.commons import clickable
from reusable_imports._css import light_scroll_area_mainwindow, dark_scroll_area_mainwindow, light_main_stylesheet, \
    dark_main_stylesheet, dark_mainwin_widget, dark_tab_widget, light_mainwin_widget, light_tab_widget, light_tab_content, dark_tab_content

# only for windows
user = ctypes.windll.user32
resolution = [user.GetSystemMetrics(0), user.GetSystemMetrics(1)]


# add code that collapses sidebar when a person clicks a button on the expand frame

class Main(QMainWindow):
    def __init__(self):
        super(Main, self).__init__()
        loadUi("UI\\ui_main.ui", self)
        self.setWindowTitle("Home - Cinematch")

        self.setMinimumWidth(resolution[0] - 20)
        self.setMinimumHeight(resolution[1] - 90)

        self.expand.hide()
        self.stack.setCurrentIndex(0)
        self.home_collapse.setChecked(True)  # By default, the home button is selected in the sidebar
        self.start_mode()

        clickable(self.collapse).connect(self.sidebar_expand_show)
        clickable(self.expand).connect(self.sidebar_collapse_show)

        self.exit_expand.clicked.connect(self.exit)
        self.exit_collapse.clicked.connect(self.exit)

        self.home_collapse.clicked.connect(self.home_func)
        self.home_expand.clicked.connect(self.home_func)

        self.findnext_collapse.clicked.connect(self.findnext_func)
        self.findnext_expand.clicked.connect(self.findnext_func)

        self.random_collapse.clicked.connect(self.random_func)
        self.random_expand.clicked.connect(self.random_func)

        self.list_collapse.clicked.connect(self.list_func)
        self.list_expand.clicked.connect(self.list_func)

        self.library_collapse.clicked.connect(self.library_func)
        self.library_expand.clicked.connect(self.library_func)

        self.add_collapse.clicked.connect(self.add_func)
        self.add_expand.clicked.connect(self.add_func)

        self.mode_collapse.clicked.connect(self.mode)
        self.mode_expand.clicked.connect(self.mode)

        self.settings_collapse.clicked.connect(self.settings_func)
        self.settings_expand.clicked.connect(self.settings_func)

        self.logout_collapse.clicked.connect(self.logout_func)
        self.logout_expand.clicked.connect(self.logout_func)

    def home_func(self):
        self.stack.setCurrentIndex(0)
        if self.expand.isVisible():
            self.expand.hide()
            self.collapse.show()

    def findnext_func(self):
        self.stack.setCurrentIndex(1)
        if self.expand.isVisible():
            self.expand.hide()
            self.collapse.show()

    def random_func(self):
        self.stack.setCurrentIndex(2)
        if self.expand.isVisible():
            self.expand.hide()
            self.collapse.show()

    def list_func(self):
        self.stack.setCurrentIndex(3)
        self.list_tabs.setCurrentIndex(0)
        if self.expand.isVisible():
            self.expand.hide()
            self.collapse.show()

    def library_func(self):
        self.stack.setCurrentIndex(4)
        if self.expand.isVisible():
            self.expand.hide()
            self.collapse.show()

    def add_func(self):
        self.stack.setCurrentIndex(5)
        if self.expand.isVisible():
            self.expand.hide()
            self.collapse.show()

    def settings_func(self):
        self.stack.setCurrentIndex(6)
        if self.expand.isVisible():
            self.expand.hide()
            self.collapse.show()

    def logout_func(self):
        # dialog box to make the user confirm if he/she wanna logs out and then call exit function
        print("Logging out")
        self.exit()

    def exit(self):
        self.close()

    def sidebar_expand_show(self):
        self.expand.show()
        self.collapse.hide()

    def sidebar_collapse_show(self):
        self.collapse.show()
        self.expand.hide()

    def start_mode(self):
        with open("Mode\\start_mode.txt", "r") as mode_file:
            mode = mode_file.readlines()

            try:
                if mode[0].strip() == "dark":
                    self.dark_mode()
                elif mode[0].strip() == "light":
                    self.light_mode()
                else:
                    self.dark_mode()

            except Exception:
                self.dark_mode()

    def mode(self):
        if self.expand.isVisible():
            self.expand.hide()
            self.collapse.show()

        with open("Mode\\mode.txt", "r") as mode_file:
            mode = mode_file.readlines()
            try:
                if mode[0].strip() == "dark":
                    self.light_mode()
                elif mode[0].strip() == "light":
                    self.dark_mode()
                else:
                    self.dark_mode()

            except Exception:
                self.dark_mode()

            mode_file.close()

    def dark_mode(self):
        with open("Mode\\mode.txt", "w") as mode:
            mode.write("dark")
            mode.close()

        with open("Mode\\start_mode.txt", "w") as mode2:
            mode2.write("dark")
            mode2.close()

        # Setting Dark Mode StyleSheets
        self.setStyleSheet(dark_main_stylesheet)
        self.home_sa_widgets.setStyleSheet(dark_scroll_area_mainwindow)
        self.search_sa_widgets.setStyleSheet(dark_scroll_area_mainwindow)
        self.settings_sa_widgets.setStyleSheet(dark_scroll_area_mainwindow)
        self.library_sa_widgets.setStyleSheet(dark_scroll_area_mainwindow)
        self.random_page.setStyleSheet(dark_mainwin_widget)
        self.add_page.setStyleSheet(dark_mainwin_widget)
        self.library_page.setStyleSheet(dark_mainwin_widget)
        self.list_tabs.setStyleSheet(dark_tab_widget)
        self.watching_tab.setStyleSheet(dark_tab_content)
        self.completed_tab.setStyleSheet(dark_tab_content)
        self.plantowatch_tab.setStyleSheet(dark_tab_content)

        self.search_button.setIcon(QIcon("Icons\\search_dark.ico"))
        self.mode_collapse.setIcon(QIcon("Icons\\dark_mode.ico"))
        self.mode_expand.setIcon(QIcon("Icons\\dark_mode.ico"))
        self.mode_expand.setText("Dark Mode")

    def light_mode(self):
        with open("Mode\\mode.txt", "w") as mode:
            mode.write("light")
            mode.close()

        with open("Mode\\start_mode.txt", "w") as mode2:
            mode2.write("light")
            mode2.close()

        # Setting Light Mode StyleSheets
        self.setStyleSheet(light_main_stylesheet)
        self.home_sa_widgets.setStyleSheet(light_scroll_area_mainwindow)
        self.search_sa_widgets.setStyleSheet(light_scroll_area_mainwindow)
        self.settings_sa_widgets.setStyleSheet(light_scroll_area_mainwindow)
        self.library_sa_widgets.setStyleSheet(light_scroll_area_mainwindow)
        self.random_page.setStyleSheet(light_mainwin_widget)
        self.add_page.setStyleSheet(light_mainwin_widget)
        self.library_page.setStyleSheet(light_mainwin_widget)
        self.list_tabs.setStyleSheet(light_tab_widget)
        self.watching_tab.setStyleSheet(light_tab_content)
        self.completed_tab.setStyleSheet(light_tab_content)
        self.plantowatch_tab.setStyleSheet(light_tab_content)

        self.search_button.setIcon(QIcon("Icons\\search_light.ico"))
        self.mode_collapse.setIcon(QIcon("Icons\\light_mode.ico"))
        self.mode_expand.setIcon(QIcon("Icons\\light_mode.ico"))
        self.mode_expand.setText("Light Mode")

    def closeEvent(self, event):
        print("closing")
        # add a dialog box that asks if the user actually want to close or not
        # or check if any bg process is running and if they are show a warning to the user


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = Main()
    window.show()

    sys.exit(app.exec_())

'''
if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = Main()
    start_win = Start()
    checklist_win = Checklist()
    genre_win = Genre()
    lang_win = Language()

    if start_win.exec_() == 1:  # User registered
        if checklist_win.exec_() == QDialog.Accepted:
            if genre_win.exec_() == QDialog.Accepted:
                if lang_win.exec_() == QDialog.Accepted:
                    window.show()
    elif start_win.exec_() == 2:  # User logged in
        window.show()

    sys.exit(app.exec_())
'''
