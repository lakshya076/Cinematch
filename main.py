import ctypes
import os
import shutil
import sys
from threading import Thread

from PyQt5.QtCore import QRect
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.uic import loadUi

from display_movie import DisplayMovies
from library import Library
from search import Search
from startup import Start
from checklist import Checklist
from genre import Genre
from language import Language

from reusable_imports._css import light_scroll_area_mainwindow, dark_scroll_area_mainwindow, light_main_stylesheet, \
    dark_main_stylesheet, dark_mainwin_widget, light_mainwin_widget
from reusable_imports.common_vars import playlists_original, playlist_picture, playlists_metadata, get_movies
from reusable_imports.commons import clickable

_thread = Thread(target=get_movies)
_thread.start()
# get_movies()  # retrieve the metadata for display

# only for windows (get resolution)
user = ctypes.windll.user32
resolution = [user.GetSystemMetrics(0), user.GetSystemMetrics(1)]


class Main(QMainWindow):
    def __init__(self):
        super(Main, self).__init__()
        loadUi("UI\\ui_main.ui", self)

        # Initial Checks
        self.setWindowTitle("Home - Cinematch")
        self.setGeometry(QRect(0, 0, resolution[0] - 20, resolution[1] - 90))
        self.expand.hide()
        self.stack.setCurrentIndex(0)
        self.home_collapse.setChecked(True)  # By default, the home button is selected in the sidebar
        self.start_mode()

        # Setting drop downs on settings page
        for i in list(playlists_metadata.values())[1:]:
            self.playlist_dd.addItem(i[0])

        clickable(self.collapse).connect(self.sidebar_expand_show)
        clickable(self.expand).connect(self.sidebar_collapse_show)

        self.exit_expand.clicked.connect(lambda: self.close())
        self.exit_collapse.clicked.connect(lambda: self.close())

        self.home_collapse.clicked.connect(self.home_func)
        self.home_expand.clicked.connect(self.home_func)

        self.findnext_collapse.clicked.connect(self.findnext_func)
        self.findnext_expand.clicked.connect(self.findnext_func)
        self.search_box.clicked.connect(self.findnext_func)
        self.search_box.returnPressed.connect(self.search_func)
        self.search_button.clicked.connect(self.search_func)

        self.random_collapse.clicked.connect(self.random_func)
        self.random_expand.clicked.connect(self.random_func)

        self.shortlist_collapse.clicked.connect(self.shortlist_func)
        self.shortlist_expand.clicked.connect(self.shortlist_func)

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

        self.clearcache_button.clicked.connect(self.clear_cache_func)
        self.delete_playlist.clicked.connect(self.deleteplay_combobox)
        self.logout_settings.clicked.connect(self.logout_func)
        self.delete_acc.clicked.connect(self.delete_acc_func)

    def search_func(self):
        search_text = self.search_box.text()
        self.search_box.clearFocus()
        self.stack.setCurrentIndex(1)
        print(f"Searching {search_text}")

    def delete_acc_func(self):
        # Dialog box to ask confirmation and give the 14-day recovery period.
        # then close the app and move the user credentials to the recovery table.
        print("Account Deleted")
        sys.exit()

    def deleteplay_combobox(self):
        play = self.playlist_dd.currentText()
        if play == "":
            pass
        else:
            # Dialog box to confirm deletion
            # get playlist index and then remove from all the common_var file's variables
            # move the whole playlist and metadata to deleted playlist table
            print("Deleted playlist")

    def clear_cache_func(self):
        cache_dir = f"{os.path.expanduser('~')}\\AppData\\Local\\Temp\\CinematchCache"
        if os.path.isdir(cache_dir):
            shutil.rmtree(cache_dir)
        else:
            print("Directory don't exist")

        self.cacheclear_label.setText("Cache cleared!")

    def home_func(self):
        self.stack.setCurrentIndex(0)
        if self.expand.isVisible():
            self.expand.hide()
            self.collapse.show()

    def findnext_func(self):
        self.stack.setCurrentIndex(1)
        self.search_box.setFocus()
        self.findnext_collapse.setChecked(True)
        if self.expand.isVisible():
            self.expand.hide()
            self.collapse.show()

    def random_func(self):
        self.stack.setCurrentIndex(2)
        if self.expand.isVisible():
            self.expand.hide()
            self.collapse.show()

    def shortlist_func(self):
        self.stack.setCurrentIndex(3)
        self.shortlist_collapse.setChecked(True)
        display = DisplayMovies("shortlist")

        def add_to_shortlist_func():
            print("Add to shortlist")

        self.add_to_shortlist.clicked.connect(lambda: add_to_shortlist_func())

        def open_movie_main():
            sender = display.sender()
            _objectdisplay = sender.objectName().strip().split(sep="_")[-1]
            print(f"Opening {_objectdisplay}")

        if len(self.shortlist_sa_widgets.children()) > 1:
            pass
        else:
            for i in range(len(display.check)):
                display.new_movies_display(name=f"{display.check[i][0].lower()}_{display.check[i][5]}",
                                           image=display.check[i][2], title=display.check[i][1],
                                           lang=display.check[i][3], pop=display.check[i][4],
                                           scroll_area=self.shortlist_sa_widgets, layout=self.shortlist_vlayout,
                                           open_movie=open_movie_main)
        if self.expand.isVisible():
            self.expand.hide()
            self.collapse.show()

    def library_func(self):
        self.stack.setCurrentIndex(4)
        children = len(playlists_metadata)
        lib = Library()

        def add_func_lib_main():
            sender = lib.sender()
            _object = sender.objectName().strip().split(sep="_")[-1]
            print(f"Add to playlist {_object}")
            # separate non-modal dialog box to add playlist

        def delete_func_lib_main():
            sender = lib.sender()
            _objectdelete = sender.objectName().strip().split(sep="_")[-1]
            if _objectdelete.lower() in ["shortlist"]:
                print("Can't Delete Pre-Built Playlist")
            else:
                print(f"Playlist Deleted {_objectdelete}")
                try:
                    del playlists_metadata[_objectdelete]
                except KeyError:
                    print("Key Error, Can't Delete Playlist.")

            self.library_func()
            # remove playlist from dict and delete the children in the library_sa and recall the lib_new_widgets func

        def open_func_lib_main():
            sender = lib.sender()
            _objectopen = sender.objectName().strip().split(sep="_")[-1]
            print(f"Opening Playlist {_objectopen}")
            if _objectopen == "shortlist":
                self.shortlist_func()
            else:
                pass
                # add functionality to open playlist in a new page

        try:
            for i in reversed(range(self.library_gridLayout.count())):
                self.library_gridLayout.itemAt(i).widget().setParent(None)
        except:
            pass

        for i in range(children):
            for j in range(1):
                lib.new_widgets_lib(name=list(playlists_metadata.keys())[i], row=j, column=i,
                                    display_name=list(playlists_metadata.values())[i][0],
                                    _username=list(playlists_metadata.values())[i][1],
                                    dob=list(playlists_metadata.values())[i][2], image=playlist_picture[i],
                                    scroll_area=self.library_sa_widgets, layout=self.library_gridLayout,
                                    add_func_lib=add_func_lib_main, delete_func_lib=delete_func_lib_main,
                                    open_func_lib=open_func_lib_main)

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
        self.cacheclear_label.setText("")
        if self.expand.isVisible():
            self.expand.hide()
            self.collapse.show()

    def logout_func(self):
        # dialog box to make the user confirm if he/she wanna logs out and then call exit function
        print("Logging out")
        self.close()

    def sidebar_expand_show(self):
        self.expand.show()
        self.collapse.hide()

    def sidebar_collapse_show(self):
        self.collapse.show()
        self.expand.hide()

    def start_mode(self):
        with open("Mode/start_mode.txt", "r") as mode_file:
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

        with open("Mode/mode.txt", "r") as mode_file:
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
        with open("Mode/mode.txt", "w") as mode:
            mode.write("dark")
            mode.close()

        with open("Mode/start_mode.txt", "w") as mode2:
            mode2.write("dark")
            mode2.close()

        # Setting Dark Mode StyleSheets
        self.setStyleSheet(dark_main_stylesheet)
        self.home_sa_widgets.setStyleSheet(dark_scroll_area_mainwindow)
        self.search_sa_widgets.setStyleSheet(dark_scroll_area_mainwindow)
        self.settings_sa_widgets.setStyleSheet(dark_scroll_area_mainwindow)
        self.library_sa_widgets.setStyleSheet(dark_scroll_area_mainwindow)
        self.shortlist_sa_widgets.setStyleSheet(dark_scroll_area_mainwindow)
        self.random_page.setStyleSheet(dark_mainwin_widget)
        self.add_page.setStyleSheet(dark_mainwin_widget)
        self.library_page.setStyleSheet(dark_mainwin_widget)
        self.shortlist_page.setStyleSheet(dark_mainwin_widget)

        self.search_button.setIcon(QIcon("Icons/search_dark.ico"))
        self.mode_collapse.setIcon(QIcon("Icons/dark_mode.ico"))
        self.mode_expand.setIcon(QIcon("Icons/dark_mode.ico"))
        self.mode_expand.setText("Dark Mode")

    def light_mode(self):
        with open("Mode/mode.txt", "w") as mode:
            mode.write("light")
            mode.close()

        with open("Mode/start_mode.txt", "w") as mode2:
            mode2.write("light")
            mode2.close()

        # Setting Light Mode StyleSheets
        self.setStyleSheet(light_main_stylesheet)
        self.home_sa_widgets.setStyleSheet(light_scroll_area_mainwindow)
        self.search_sa_widgets.setStyleSheet(light_scroll_area_mainwindow)
        self.settings_sa_widgets.setStyleSheet(light_scroll_area_mainwindow)
        self.library_sa_widgets.setStyleSheet(light_scroll_area_mainwindow)
        self.shortlist_sa_widgets.setStyleSheet(light_scroll_area_mainwindow)
        self.random_page.setStyleSheet(light_mainwin_widget)
        self.add_page.setStyleSheet(light_mainwin_widget)
        self.library_page.setStyleSheet(light_mainwin_widget)
        self.shortlist_page.setStyleSheet(light_mainwin_widget)

        self.search_button.setIcon(QIcon("Icons/search_light.ico"))
        self.mode_collapse.setIcon(QIcon("Icons/light_mode.ico"))
        self.mode_expand.setIcon(QIcon("Icons/light_mode.ico"))
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
