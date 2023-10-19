import ctypes
import os
import shutil
import sys
import random
from threading import Thread

import pymysql
import requests
from PyQt5.QtCore import QRect
from PyQt5.QtGui import QIcon, QImage, QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QWidget, QVBoxLayout, QScrollArea, QHBoxLayout
from PyQt5.uic import loadUi
from cachecontrol import CacheControl
from cachecontrol.caches import FileCache

from display_movie import DisplayMovies
from library import Library
from search import Search
from startup import Start
from checklist import Checklist
from genre import Genre
from language import Language

from reusable_imports._css import light_scroll_area_mainwindow, dark_scroll_area_mainwindow, light_main_stylesheet, \
    dark_main_stylesheet, dark_mainwin_widget, light_mainwin_widget
from reusable_imports.common_vars import playlist_picture, playlists_metadata, get_movies, removed_playlists, \
    playlists_display_metadata, random_movies, iso_639_1
from reusable_imports.commons import clickable
from utils.movie_utils import get_title, get_poster, get_overview, get_genz, get_release_date, get_lang, get_pop

# MAKE A MOVIE DELETE FUNCTIONALITY FOR PLAYLISTS OTHER THAN SHORTLIST
# FIX ADD TO SHORTLIST BUTTON (OR MAKE A SEPARATE WINDOW FOR IT)
# FIX ADD TO SHORTLIST ON RANDOM SCREEN

# Threading to get the movies metadata (movies stored in playlists) at start
_thread = Thread(target=get_movies)
_thread.start()

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
        self.random_movie()

        # List to keep the check of how many playlist widgets have been created in the stack
        self.widget_created_ind = dict()

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

        self.randomiser.clicked.connect(lambda: self.random_movie())
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

    def random_movie(self):
        self.random_id = random.choice(random_movies)
        conn = pymysql.connect(host='localhost', user='root', password='root', database='movies')
        cache_path = f"{os.path.expanduser('~')}\\AppData\\Local\\Temp\\CinematchCache\\.main_img_cache"
        session = CacheControl(requests.Session(), cache=FileCache(cache_path))

        # get_title, get_poster, get_overview, get_genz, get_release_date, get_lang, get_pop
        random_title = get_title(self.random_id, conn, conn.cursor())
        random_poster = get_poster(self.random_id, conn, conn.cursor())
        random_overview = get_overview(self.random_id, conn, conn.cursor())
        random_lang = get_lang(self.random_id, conn, conn.cursor())
        random_pop = get_pop(self.random_id, conn, conn.cursor())
        random_gen = get_genz(self.random_id, conn, conn.cursor())
        random_date = get_release_date(self.random_id, conn, conn.cursor())

        if random_overview == "nan":
            random_overview = "Not Available"

        try:
            random_lang_real = iso_639_1[random_lang]
        except KeyError:
            random_lang_real = random_lang

        random_genre_real = str()
        for i in random_gen:
            random_genre_real += f"{i}, "

        random_poster_real = session.get(f"https://image.tmdb.org/t/p/original{random_poster}").content
        image_object = QImage()
        image_object.loadFromData(random_poster_real)

        self.random_image.setPixmap(QPixmap(image_object))
        self.random_title.setText(random_title)
        self.random_overview.setText(random_overview)
        self.random_pop.setText(f"Popularity:\n{str(random_pop)}")
        self.random_lang.setText(random_lang_real)
        self.random_genre.setText(random_genre_real[:-2:1])
        self.random_date.setText(str(random_date))

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

        def open_movie_main():
            sender = display.sender()
            _objectdisplay = sender.objectName().strip().split(sep="_")[-1]
            print(f"Opening {_objectdisplay}")

        def delete_movie_main():
            sender = display.sender()
            _playlist = sender.objectName().strip().split(sep="_")[-2]
            _objectdelete = sender.objectName().strip().split(sep="_")[-1]

            try:
                delete_list = [i[5] for i in display.check]
                delete_queue = delete_list.index(int(_objectdelete))
                del playlists_display_metadata[_playlist][delete_queue]
                print(f"Movie Deleted {_objectdelete} from {_playlist}")
                # Reflect changes in sql table
            except KeyError:
                print("Key Error, Can't Delete Playlist.")

            self.shortlist_func()
            # remove move from playlist and recall shortlist_func function to reload the widgets

        try:
            for i in reversed(range(self.shortlist_vlayout.count())):
                self.shortlist_vlayout.itemAt(i).widget().setParent(None)
        except:
            pass

        for i in range(len(display.check)):
            display.new_movies_display(name=f"{display.check[i][0].lower()}_{display.check[i][5]}",
                                       image=display.check[i][2], title=display.check[i][1],
                                       lang=display.check[i][3], pop=display.check[i][4],
                                       scroll_area=self.shortlist_sa_widgets, layout=self.shortlist_vlayout,
                                       open_movie=open_movie_main, delete_movie=delete_movie_main)
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
            # redirect to add playlist stack page

        def delete_func_lib_main():
            sender = lib.sender()
            _objectdelete = sender.objectName().strip().split(sep="_")[-1]
            if _objectdelete.lower() in ["shortlist"]:
                print("Can't Delete Pre-Built Playlist")
            else:
                try:
                    removed_playlists[_objectdelete] = playlists_metadata[_objectdelete]
                    del playlists_metadata[_objectdelete]
                    print(f"Playlist Deleted {_objectdelete}")
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
                self.open_playlist_func(_objectopen)
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

    def open_playlist_func(self, playlist_name: str):

        if playlist_name in self.widget_created_ind.keys():
            self.stack.setCurrentIndex(self.widget_created_ind[playlist_name])
        else:
            self.frame_name = QWidget()
            self.frame_name.setObjectName(playlist_name)
            self.frame_name.setStyleSheet(dark_mainwin_widget)
            setattr(self, playlist_name, self.frame_name)

            self.name_label = QLabel(self.frame_name)
            self.name_label.setText(f"{playlists_metadata[playlist_name][0]}")
            self.name_label.setStyleSheet("font:20pt;")

            self.frame_vert_layout = QVBoxLayout(self.frame_name)
            self.frame_hor_layout = QHBoxLayout()
            self.frame_hor_layout.addWidget(self.name_label)

            self.frame_display_sa = QScrollArea(self.frame_name)
            self.frame_display_sa.setObjectName(f"sa_{playlist_name}")
            self.frame_display_sa.setWidgetResizable(True)

            self.frame_display_sa_widgets = QWidget()
            self.frame_display_sa_widgets.setObjectName(f"sa_widgets_{playlist_name}")
            self.frame_display_sa_widgets.setGeometry(QRect(0, 0, 820, 439))
            self.frame_display_sa_widgets.setStyleSheet("background-color:#24292e; color:#fffaf0;")

            self.frame_display_vlayout = QVBoxLayout(self.frame_display_sa_widgets)
            self.frame_display_vlayout.setObjectName(u"frame_display_vlayout")
            self.frame_display_sa.setWidget(self.frame_display_sa_widgets)

            self.frame_vert_layout.addLayout(self.frame_hor_layout)
            self.frame_vert_layout.addWidget(self.frame_display_sa)

            display = DisplayMovies(playlist_name)

            def open_movie_main():
                sender = display.sender()
                _objectdisplay = sender.objectName().strip().split(sep="_")[-1]
                print(f"Opening {_objectdisplay}")

            def delete_movie_main():
                # Make a remove function for playlists other than shortlist
                sender = display.sender()
                _objectdisplay = sender.objectName().strip().split(sep="_")[-1]
                print(f"Removing {_objectdisplay}")

            try:
                for i in reversed(range(self.frame_display_vlayout.count())):
                    self.frame_display_vlayout.itemAt(i).widget().setParent(None)
            except:
                pass

            for i in range(len(display.check)):
                display.new_movies_display(name=f"{display.check[i][0].lower()}_{display.check[i][5]}",
                                           image=display.check[i][2], title=display.check[i][1],
                                           lang=display.check[i][3], pop=display.check[i][4],
                                           scroll_area=self.frame_display_sa_widgets, layout=self.frame_display_vlayout,
                                           open_movie=open_movie_main, delete_movie=delete_movie_main)

            self.stack.addWidget(self.frame_name)
            self.stack.setCurrentWidget(self.frame_name)
            index = self.stack.currentIndex()
            self.widget_created_ind[playlist_name] = index

            print(self.frame_name.objectName())

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
        # Commit ALL THE CHANGES that happened in the common_vars.py file like if playlist is deleted or movie is
        # deleted from playlist or a new movie playlist is created
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
