import ctypes
import datetime
import os
import shutil
import sys
import random
import platform

import requests
import PyQt5
from PyQt5.QtCore import QRect, QObject, pyqtSignal, QThread, QSize, Qt
from PyQt5.QtGui import QIcon, QImage, QPixmap, QKeySequence, QMovie, QGuiApplication
from PyQt5.QtWidgets import QMainWindow, QApplication, QDialog, QShortcut, QMessageBox, QLabel
from PyQt5.uic import loadUi

from display_movie import DisplayMovies
from library import Library
from splash_screen import SplashScreen
from widget_generator_home import Home
from startup import Start
from checklist import Checklist
from genre import Genre
from language import Language

from reusable_imports._css import light_scroll_area_mainwindow, dark_scroll_area_mainwindow, light_main_stylesheet, \
    dark_main_stylesheet, dark_mainwin_widget, light_mainwin_widget
from reusable_imports.common_vars import *
from reusable_imports.commons import clickable, remove_spaces
from backend.Utils.movie_utils import *
from backend import playlists, users, movie_search
from widget_generator_search import SearchMovies

# Checking OS
if platform.system() == "Windows":
    print("OS check completed")
else:
    print("This program only works on Windows systems")
    sys.exit(-2)

# only for windows (get resolution)
user = ctypes.windll.user32
resolution = [user.GetSystemMetrics(0), user.GetSystemMetrics(1)]

searched_movies = []
search_text = ""


class SearchAlg(QObject):
    done = pyqtSignal()

    def run(self):
        global searched_movies, search_text

        print(f"Searching {search_text}")
        searched_movies = movie_search.search(search_text, cur)[:10]
        print(f'Search Results: {searched_movies}')

        for i in get_movies_info(searched_movies, cur):
            title = i[1] or "Not Available"  # gets title
            overview = i[2] or "Not Available"
            date = i[3]
            gen = i[4] or "Not Available"
            lang = i[5] or "Not Available"
            pop = i[6] or "Not Available"
            cast = i[7] or "Not Available"
            poster_path = i[8]  # gets poster path

            genre_real = "Not Available"
            lang_real = ""

            # Formatting date
            try:
                real_date = datetime.datetime.strptime(str(date), "%Y-%m-%d").strftime("%m-%d-%Y")
            except ValueError:
                real_date = "Not Available"

            # Formatting genre
            if gen != "Not Available":
                genre_real = ", ".join(gen)

            # Formatting poster path
            if poster_path != 'nan' and poster_path:
                try:
                    poster_var = session.get(f"https://image.tmdb.org/t/p/original{poster_path}").content
                except requests.ConnectionError:  # Network Error
                    poster_var = not_found_img
                # gets poster image as a byte array
            else:
                poster_var = not_found_img
                # executes if the poster path is not available in the database.

            # Formatting language
            if lang != "Not Available":
                try:
                    lang_real = iso_639_1[lang]
                except KeyError:
                    lang_real = lang

            metadata_enter = [title, overview, real_date, genre_real, lang_real, str(pop), cast, poster_var]

            if i[0] not in movies_metadata:
                movies_metadata[int(i[0])] = metadata_enter

        self.done.emit()


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
        self.movie_disp(random_movies, _image=self.random_image, _title=self.random_title,
                        _overview=self.random_overview, _pop=self.random_pop, _lang=self.random_lang,
                        _genre=self.random_genre, _date=self.random_date, _shortlist_but=self.random_add_toshortlist)
        self.user_settings.setText(username)

        # Hiding widgets if user has premium
        if premium == 1:
            self.premium.hide()
            self.ad_search.hide()
            self.ad_create.hide()
        elif premium == 0:
            self.premium.show()
            self.ad_search.show()
            self.ad_create.show()

        # Setting shortcut for search box
        self.shortcut = QShortcut(QKeySequence("Alt+D"), self)
        self.shortcut.activated.connect(self.search_shortcut)

        clickable(self.collapse).connect(self.sidebar_expand_show)
        clickable(self.expand).connect(self.sidebar_collapse_show)

        # Setting function calls when their corresponding buttons are clicked in the sidebar.
        self.exit_expand.clicked.connect(lambda: self.close())
        self.exit_collapse.clicked.connect(lambda: self.close())

        self.home_collapse.clicked.connect(self.home_func)
        self.home_expand.clicked.connect(self.home_func)

        self.findnext_collapse.clicked.connect(self.findnext_func)
        self.findnext_expand.clicked.connect(self.findnext_func)
        self.search_box.clicked.connect(self.findnext_func)
        self.search_box.returnPressed.connect(self.search_func)
        self.search_button.clicked.connect(self.search_func)

        # Loading GIF and Threading in Search Window
        self.loading = QMovie("Images/loading.gif")
        self.label = QLabel()
        self.label.setFixedSize(QSize(64, 64))
        self.label.setScaledContents(True)
        self.label.setMovie(self.loading)
        self.search_sa_real_hlayout.addWidget(self.label)

        self.thread = QThread()
        self.worker = SearchAlg()
        self.worker.moveToThread(self.thread)
        self.worker.done.connect(self.search_put)
        self.thread.started.connect(self.worker.run)

        self.randomiser.clicked.connect(self.placeholder_random)  # Randomise movie
        self.random_collapse.clicked.connect(self.random_func)
        self.random_expand.clicked.connect(self.random_func)

        self.shortlist_collapse.clicked.connect(self.shortlist_func)
        self.shortlist_expand.clicked.connect(self.shortlist_func)

        self.library_collapse.clicked.connect(self.library_func)
        self.library_expand.clicked.connect(self.library_func)

        self.create_collapse.clicked.connect(self.create_func)
        self.create_expand.clicked.connect(self.create_func)
        self.create_playlist.clicked.connect(self.create_playlist_func)
        self.create_playlist_name.returnPressed.connect(self.create_playlist_func)

        # Credit/License, Premium, Ads
        self.credit_license.clicked.connect(self.credit_license_func)
        self.premium.clicked.connect(self.premium_func)
        self.premium_plans.clicked.connect(self.premium_plans_func)
        self.ad_create.setPixmap(QPixmap(random.choice(ad)))
        self.ad_search.setPixmap(QPixmap(random.choice(ad)))

        self.mode_collapse.clicked.connect(self.mode)
        self.mode_expand.clicked.connect(self.mode)

        self.settings_collapse.clicked.connect(self.settings_func)
        self.settings_expand.clicked.connect(self.settings_func)

        self.logout_collapse.clicked.connect(self.logout_func)
        self.logout_expand.clicked.connect(self.logout_func)

        self.clearcache_button.clicked.connect(self.clear_cache_func)
        self.logout_settings.clicked.connect(self.logout_func)
        self.delete_acc.clicked.connect(self.delete_acc_func)

        # Displaying widgets on the home screen
        home = Home()
        if len(recoms) != 0:
            for i in range(len(recoms)):
                home.new_widgets_home(recoms[i], title=movies_metadata[recoms[i]][0],
                                      image=movies_metadata[recoms[i]][7], scroll_area=self.foryou_sa_widgets,
                                      layout=self.foryou_hlayout, open_func_lib=self.open_home_search)
        if len(watchagain) != 0:
            for i in range(len(watchagain)):
                home.new_widgets_home(watchagain[i], image=movies_metadata[watchagain[i]][7],
                                      title=movies_metadata[watchagain[i]][0], scroll_area=self.watchagain_sa_widgets,
                                      layout=self.watchagain_hlayout, open_func_lib=self.open_home_search)
        if len(language) != 0:
            for i in range(len(language)):
                home.new_widgets_home(language[i], title=movies_metadata[language[i]][0],
                                      image=movies_metadata[language[i]][7], scroll_area=self.languages_sa_widgets,
                                      layout=self.languages_hlayout, open_func_lib=self.open_home_search)

    def home_func(self):
        """
        Function to switch to the home widget in the stack
        """
        self.stack.setCurrentIndex(0)
        if self.expand.isVisible():
            self.expand.hide()
            self.collapse.show()

    def findnext_func(self):
        """
        Function to switch to the search widget in the stack
        """
        self.stack.setCurrentIndex(1)
        self.search_box.setFocus()
        self.findnext_collapse.setChecked(True)
        if self.expand.isVisible():
            self.expand.hide()
            self.collapse.show()

    def random_func(self):
        """
        Function to switch to the random widget in the stack
        """
        self.stack.setCurrentIndex(2)
        if self.expand.isVisible():
            self.expand.hide()
            self.collapse.show()

    def shortlist_func(self):
        """
        Function to switch to the shortlist widget in the stack
        """
        self.stack.setCurrentIndex(3)
        self.shortlist_collapse.setChecked(True)
        display = DisplayMovies("shortlist")

        def open_movie_main():
            """
            Opens the clicked movie on the shortlist page
            Function is passed a parameter in display_new_widgets function of DisplayMovies class
            """
            sender = display.sender()
            _objectdisplay = sender.objectName().strip().split(sep="_")[-1]
            try:
                display_id = int(_objectdisplay)
                self.movie_disp([display_id], _image=self.display_image, _title=self.display_title,
                                _overview=self.display_overview, _pop=self.display_pop, _lang=self.display_lang,
                                _genre=self.display_genre, _date=self.display_date,
                                _shortlist_but=self.display_add_toshortlist)
                self.stack.setCurrentIndex(7)
            except TypeError:
                print("TypeError. Can't display movie.")

        def delete_movie_main():
            """
            Deletes the clicked movie from the shortlist page and then refreshes it to show the updated shortlist
            Function is passed a parameter in display_new_widgets function of DisplayMovies class
            """
            sender = display.sender()
            _playlist = sender.objectName().strip().split(sep="_")[-2]
            _objectdelete = sender.objectName().strip().split(sep="_")[-1]
            _playlist_name = playlists_metadata[_playlist][0]

            try:
                delete_list = [i[5] for i in display.check]
                delete_queue = delete_list.index(int(_objectdelete))
                # Deletes from the viewable 'client' side dict
                del playlists_display_metadata[_playlist][delete_queue]

                # Deletes from the backend list which will be updated in the sql table
                print(playlists_metadata)
                print(_playlist, _objectdelete)
                removed_playlist_movies[_playlist_name].append(int(_objectdelete))
                playlists_metadata[_playlist][3].remove(int(_objectdelete))

                print(f"Movie Deleted {_objectdelete} from {_playlist}")
                # Reflect changes in sql table
            except KeyError as e:
                print(f"{e}, Can't Delete Playlist.")

            self.shortlist_func()
            # remove from shortlist and recall shortlist_func function to reload the widgets in the shortlist page

        try:
            # Removes the previously generated widgets and sets the layout empty
            for i in reversed(range(self.shortlist_vlayout.count())):
                self.shortlist_vlayout.itemAt(i).widget().setParent(None)
        except:
            print("Can't delete movie layout")

        # Add new widgets after the previously generated widgets are removed
        for i in range(len(display.check)):
            display.new_movies_display(name=f"{display.check[i][0].lower()}_{display.check[i][5]}",
                                       image=display.check[i][2], title=display.check[i][1],
                                       lang=display.check[i][3], pop=display.check[i][4],
                                       scroll_area=self.shortlist_sa_widgets, layout=self.shortlist_vlayout,
                                       open_movie=open_movie_main, delete_movie=delete_movie_main,
                                       p_md=playlists_metadata)
        if self.expand.isVisible():
            self.expand.hide()
            self.collapse.show()

    def library_func(self):
        """
        Function to switch to the library widget in the stack
        The library widget displays all the playlists
        """
        self.stack.setCurrentIndex(4)
        children = len(playlists_metadata)
        lib = Library()

        def delete_func_lib_main():
            """
            Deletes the clicked playlist from the library page and then refreshes it to show the updated library
            Function is passed a parameter in new_widgets_lib function of Library class
            """
            sender = lib.sender()
            _objectdelete = sender.objectName().strip().split(sep="_")[-1]  # gets the name of the playlist to delete
            if _objectdelete.lower() in ["shortlist"]:
                print("Can't Delete Pre-Built Playlist")
            else:
                try:
                    # Try to delete playlist
                    removed_playlists[_objectdelete] = playlists_metadata[_objectdelete][0]
                    playlist_name = playlists_metadata[_objectdelete][0]
                    print(playlist_name)
                    del playlists_metadata[_objectdelete]

                    print(f"Playlist Deleted {_objectdelete}")

                except KeyError:
                    print("Key Error, Can't Delete Playlist.")

            self.library_func()
            # remove playlist from dict and delete the children in the library_sa and recall the lib_new_widgets func to
            # reflect changes

        def open_func_lib_main():
            """
            Opens the playlist from the library page
            Function is passed a parameter of new_widgets_lib function of Library class
            """
            sender = lib.sender()
            _objectopen = sender.objectName().strip().split(sep="_")[-1]  # gets the name of the playlist to open
            print(f"Opening Playlist {_objectopen}")
            if _objectopen == "shortlist":
                self.shortlist_func()  # opens the shortlist page if playlist is shortlist
            else:
                self.open_playlist_func(_objectopen)
                # opens the playlist in a new dynamically controlled page

        try:
            # Tries to remove the current widgets in the library grid layout
            for i in reversed(range(self.library_gridLayout.count())):
                self.library_gridLayout.itemAt(i).widget().setParent(None)
        except:
            print("Can't delete playlist layout")

        # Adds the new widgets to the library grid layout
        print(playlist_picture)
        # TODO Define the for loop properly
        for i in range(children):
            for j in range(1):
                lib.new_widgets_lib(name=list(playlists_metadata.keys())[i], row=j, column=i,
                                    display_name=list(playlists_metadata.values())[i][0],
                                    _username=list(playlists_metadata.values())[i][1],
                                    dob=list(playlists_metadata.values())[i][2], image=playlist_picture[i],
                                    scroll_area=self.library_sa_widgets, layout=self.library_gridLayout,
                                    delete_func_lib=delete_func_lib_main, open_func_lib=open_func_lib_main)

        if self.expand.isVisible():
            self.expand.hide()
            self.collapse.show()

    def create_func(self):
        """
        Function to display the add (create) playlist widget of the stack
        """
        self.playlist_error.setText("")
        self.playlist_success.setText("")
        self.create_playlist_name.clear()

        self.stack.setCurrentIndex(5)
        if self.expand.isVisible():
            self.expand.hide()
            self.collapse.show()

    def settings_func(self):
        """
        Function to display the settings widget of the stack
        """
        self.stack.setCurrentIndex(6)
        self.cacheclear_label.setText("")
        if self.expand.isVisible():
            self.expand.hide()
            self.collapse.show()

    def logout_func(self):
        """
        Function to log out the user.
        Produces a simple dialog box to ask for confirmation.
        """

        reply = QMessageBox.question(self, "Logout", "Are you sure you want to logout?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            users.logout(cur, conn)
            print("Logging out")
            self.close()
        elif reply == QMessageBox.No:
            print("Logout Aborted")

    def search_shortcut(self):
        """
        Function to activate search box by clicking shortcut Alt+D
        """
        self.findnext_func()
        self.search_box.selectAll()

    def open_home_search(self):
        """
        Function to open movies on home page and search page
        """
        sender = self.sender()
        _id = sender.objectName().split(sep="_")[-1]

        try:
            self.movie_disp([int(_id)], _image=self.display_image, _title=self.display_title,
                            _overview=self.display_overview, _pop=self.display_pop, _lang=self.display_lang,
                            _genre=self.display_genre, _date=self.display_date,
                            _shortlist_but=self.display_add_toshortlist)
            self.stack.setCurrentIndex(7)
        except TypeError:
            print(f"Can't display {_id}")

    def open_playlist_func(self, playlist_name: str):
        """
        The actual function to open a playlist
        This function displays the playlist in the 9th window (index=8) of the stack
        """

        display = DisplayMovies(playlist_name)

        def open_movie_main():
            """
            Displays the movie clicked in the playlist
            """
            sender = display.sender()
            _objectdisplay = sender.objectName().strip().split(sep="_")[-1]
            try:
                display_id = int(_objectdisplay)
                self.movie_disp([display_id], _image=self.display_image, _title=self.display_title,
                                _overview=self.display_overview, _pop=self.display_pop, _lang=self.display_lang,
                                _genre=self.display_genre, _date=self.display_date,
                                _shortlist_but=self.display_add_toshortlist)
                self.stack.setCurrentIndex(7)
            except TypeError:
                print("TypeError. Can't display movie.")

        def delete_movie_main():
            """
            Deletes the clicked movie from the playlist page and then refreshes it to show the updated playlist
            Function is passed a parameter in display_new_widgets function of DisplayMovies class
            """
            sender = display.sender()
            _playlist = sender.objectName().strip().split(sep="_")[-2]
            _playlist_name = playlists_metadata[_playlist][0]
            _objectdelete = sender.objectName().strip().split(sep="_")[-1]

            try:
                delete_list = [i[5] for i in display.check]
                delete_queue = delete_list.index(int(_objectdelete))
                # Deletes from the viewable 'client' side dict
                del playlists_display_metadata[_playlist][delete_queue]
                removed_playlist_movies[_playlist_name].append(int(_objectdelete))
                playlists_metadata[_playlist][3].remove(int(_objectdelete))
                print("Can't delete")

                print(f"Movie Deleted {_objectdelete} from {_playlist}")
                # Reflect changes in sql table
            except Exception as e:
                print(f"{e} Can't Delete Playlist.")

            self.open_playlist_func(playlist_name=playlist_name)
            # remove from shortlist and recall shortlist_func function to reload the widgets in the shortlist page

        try:
            # Removes the previously generated widgets and sets the layout empty
            for i in reversed(range(self.playlist_vlayout.count())):
                self.playlist_vlayout.itemAt(i).widget().setParent(None)
        except:
            print("Can't delete movie layout")

        for i in range(len(display.check)):
            display.new_movies_display(name=f"{display.check[i][0].lower()}_{display.check[i][5]}",
                                       image=display.check[i][2], title=display.check[i][1],
                                       lang=display.check[i][3], pop=display.check[i][4],
                                       scroll_area=self.playlist_sa_widgets, layout=self.playlist_vlayout,
                                       open_movie=open_movie_main, delete_movie=delete_movie_main,
                                       p_md=playlists_metadata)
        self.playlist_name.setText(f"{playlists_metadata[playlist_name][0]}")

        self.stack.setCurrentIndex(8)

    def create_playlist_func(self):
        """
        Function to create a playlist and add it to playlist_metadata list
        """
        self.playlist_error.setText("")
        self.playlist_success.setText("")

        text = self.create_playlist_name.text()
        uid = remove_spaces(text)
        current_date = datetime.date.today().strftime("%d/%m/%Y")

        if text == "":
            self.playlist_error.setText("Please enter playlist name")
        elif len(text) > 18:
            self.playlist_error.setText("Playlist name can not be over 18 characters")
        elif uid in playlists_metadata.keys():
            self.playlist_error.setText("Playlist name not available!")
        elif len(playlists_metadata.keys()) == 10 and premium == 0:
            self.playlist_error.setText("Maximum 10 playlists allowed. Go Premium to get more playlists")
        else:
            playlists_metadata[uid] = [text, username, current_date, []]
            playlists_display_metadata[uid] = []  # manually adding playlist to the display metadata variable
            playlist_picture.append(random.choice(poster))
            try:
                playlists.create_playlist(username, uid, '', '', conn, cur)
                self.playlist_success.setText("Playlist added to account.")
            except:
                self.playlist_error.setText("Unable to add playlist")

    def placeholder_random(self):
        self.movie_disp(random_movies, _image=self.random_image, _title=self.random_title,
                        _overview=self.random_overview, _pop=self.random_pop, _lang=self.random_lang,
                        _genre=self.random_genre, _date=self.random_date,
                        _shortlist_but=self.random_add_toshortlist)

    def movie_disp(self, id: list, _image: PyQt5.QtWidgets.QLabel, _title: PyQt5.QtWidgets.QLabel,
                   _overview: PyQt5.QtWidgets.QTextBrowser, _pop: PyQt5.QtWidgets.QLabel, _lang: PyQt5.QtWidgets.QLabel,
                   _genre: PyQt5.QtWidgets.QLabel, _date: PyQt5.QtWidgets.QLabel,
                   _shortlist_but: PyQt5.QtWidgets.QPushButton):
        """
        Function to display movies when the respective movie frame is clicked
        """
        _id = random.choice(id)

        title = ""
        overview = ""
        date = ""
        gen = ""
        lang = ""
        pop = ""
        cast = ""
        poster = ""

        try:
            movie = movies_metadata[_id]
            title = movie[0]
            overview = movie[1]
            date = movie[2]
            gen = movie[3]
            lang = movie[4]
            pop = movie[5]
            cast = movie[6]
            poster = movie[7]

        except KeyError:
            print("Unable to display movie")

        # Formatting poster
        image_object = QImage()  # initialising a QImage object
        image_object.loadFromData(poster)  # parameter of function (reference to the for loop in __init__ method)
        image_to_load = QPixmap(image_object)  # converting QImage object to QPixmap object to display on the label

        def add_to_shortlist():
            """
            Function to add a movie to shortlist
            """
            _shortlist_but.disconnect()  # To prevent multiple signals get connected to the clicked button
            _shortlist_but.setDisabled(True)

            playlists_metadata["shortlist"][3].append(_id)
            print(f"Added {_id} to shortlist")

            enter = ["Shortlist", title, poster, lang, pop, _id]

            playlists_display_metadata["shortlist"].append(tuple(enter))
            print(f"Added {_id} to display list")

        _image.setPixmap(image_to_load)
        _title.setText(title)
        _overview.setText(overview)
        _pop.setText(f"Popularity:\n{str(pop)}")
        _lang.setText(lang)
        _genre.setText(gen)
        _date.setText(f"Release Date:\n{date}")

        _shortlist_but.setChecked(False)
        _shortlist_but.clicked.connect(lambda: add_to_shortlist())
        _shortlist_but.setEnabled(True)

    def search_func(self):
        """
        Function to search and display movies in the search widget of the stack.
        """
        global search_text
        search_text = self.search_box.text()
        self.search_box.clearFocus()  # Removes focus from the search box
        self.stack.setCurrentIndex(1)  # Sets stack's current index to the index corresponding to the search widget

        self.thread.start()

        try:
            for i in reversed(range(self.search_sa_real_hlayout.count())):
                if i == 0:
                    break
                self.search_sa_real_hlayout.itemAt(i).widget().setParent(None)
        except:
            pass

        if not self.label.isVisible():
            self.label.show()
            self.loading.start()
        else:
            self.loading.start()

    def search_put(self):
        self.loading.stop()
        self.label.hide()
        self.thread.quit()
        self.thread.exit()

        if len(searched_movies) != 0:
            search = SearchMovies()

            for i in range(len(searched_movies)):
                _id = searched_movies[i]

                search.new_widgets_search(_id, title=movies_metadata[_id][0], image=movies_metadata[_id][7],
                                          scroll_area=self.search_sa_real_widgets,
                                          layout=self.search_sa_real_hlayout, open_func_lib=self.open_home_search)

    def credit_license_func(self):
        """
        Function to open Credits/License Window
        """
        self.stack.setCurrentIndex(9)
        if self.expand.isVisible():
            self.expand.hide()
            self.collapse.show()

    def premium_func(self):
        """
        Function to open Premium Window if user doesn't have premium
        """
        self.stack.setCurrentIndex(10)
        if self.expand.isVisible():
            self.expand.hide()
            self.collapse.show()

    def premium_plans_func(self):
        """
        Function to display premium plans
        """
        print("Checking Available Premium Plans")

    def delete_acc_func(self):
        """
        Function to delete user's account (move it to recovery table)
        """
        # TODO ask for confirmation and warn user about waiting period. Ask for password as confirmation if possible
        # TODO Return to login menu

        users.delete_user(username, conn, cur)
        print("Account Deleted")
        self.close()

    def clear_cache_func(self):
        """
        Clear cache to improve performance. Restart app to see effective changes.
        """
        cache_dir = f"{os.path.expanduser('~')}\\AppData\\Local\\Temp\\CinematchCache"
        if os.path.isdir(cache_dir):
            shutil.rmtree(cache_dir)
        else:
            print("Directory don't exist")

        self.cacheclear_label.setText("Cache cleared!")

    def sidebar_expand_show(self):
        """
        Function to show the expanded sidebar and hide the collapsed sidebar
        """
        self.expand.show()
        self.collapse.hide()

    def sidebar_collapse_show(self):
        """
        Function to short the collapsed sidebar and hide the expanded sidebar
        """
        self.collapse.show()
        self.expand.hide()

    def start_mode(self):
        """
        Function to check the mode (theme) of the app when opened to set the respective mode
        """
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
                # If any issues, dark mode is put by default
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
        """
        Function to change to dark mode
        """
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
        self.playlist_sa_widgets.setStyleSheet(dark_scroll_area_mainwindow)
        self.credit_license_sa_widgets.setStyleSheet(dark_scroll_area_mainwindow)
        self.premium_sa_widgets.setStyleSheet(dark_scroll_area_mainwindow)
        self.random_page.setStyleSheet(dark_mainwin_widget)
        self.create_page.setStyleSheet(dark_mainwin_widget)
        self.library_page.setStyleSheet(dark_mainwin_widget)
        self.shortlist_page.setStyleSheet(dark_mainwin_widget)
        self.display_page.setStyleSheet(dark_mainwin_widget)
        self.playlist_page.setStyleSheet(dark_mainwin_widget)
        self.credit_license_page.setStyleSheet(dark_mainwin_widget)
        self.premium_page.setStyleSheet(dark_mainwin_widget)

        self.search_button.setIcon(QIcon("Icons/search_dark.ico"))
        self.mode_collapse.setIcon(QIcon("Icons/dark_mode.ico"))
        self.mode_expand.setIcon(QIcon("Icons/dark_mode.ico"))
        self.mode_expand.setText("Dark Mode")

        self.user_img.setPixmap(QPixmap("Images/user_white.png"))
        self.user_settings.setStyleSheet("color:#fffaf0;font:18pt;")

        self.credit_license.setIcon(QIcon("Icons/license_white.png"))
        self.premium.setStyleSheet("font:12pt;background-color:rgba(0,0,0,0);color:#fffaf0;")

    def light_mode(self):
        """
        Function to change to light mode
        """
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
        self.playlist_sa_widgets.setStyleSheet(light_scroll_area_mainwindow)
        self.credit_license_sa_widgets.setStyleSheet(light_scroll_area_mainwindow)
        self.premium_sa_widgets.setStyleSheet(light_scroll_area_mainwindow)
        self.random_page.setStyleSheet(light_mainwin_widget)
        self.create_page.setStyleSheet(light_mainwin_widget)
        self.library_page.setStyleSheet(light_mainwin_widget)
        self.shortlist_page.setStyleSheet(light_mainwin_widget)
        self.display_page.setStyleSheet(light_mainwin_widget)
        self.playlist_page.setStyleSheet(light_mainwin_widget)
        self.credit_license_page.setStyleSheet(light_mainwin_widget)
        self.premium_page.setStyleSheet(light_mainwin_widget)

        self.search_button.setIcon(QIcon("Icons/search_light.ico"))
        self.mode_collapse.setIcon(QIcon("Icons/light_mode.ico"))
        self.mode_expand.setIcon(QIcon("Icons/light_mode.ico"))
        self.mode_expand.setText("Light Mode")

        self.user_img.setPixmap(QPixmap("Images/user_black.png"))
        self.user_settings.setStyleSheet("color:#000;font:18pt;")

        self.credit_license.setIcon(QIcon("icons/license_black.png"))
        self.premium.setStyleSheet("font:12pt;background-color:rgba(0,0,0,0);color:#000000;")

    def closeEvent(self, event):
        print("closing")
        print(playlists_metadata)
        print(removed_playlists)
        # playlist metadata will be pushed to the sql table which contains information about all the playlists made by the user
        # removed playlists will be pushed to the deleted playlist table from where the user can recover it if wanted
        # Commit ALL THE CHANGES that happened in the common_vars.py file like if playlist is deleted or movie is
        # deleted from playlist or a new movie playlist is created
        # add a dialog box that asks if the user actually want to close or not
        # or check if any bg process is running and if they are show a warning to the user

        for i in playlists_metadata.keys():
            playlists.add_movies(playlists_metadata[i][3], username, playlists_metadata[i][0], conn, cur)

        for i in removed_playlist_movies.keys():
            playlists.remove_movies(removed_playlist_movies[i], username, i, conn, cur)

        for i in removed_playlists.values():
            playlists.delete_playlist(username, i, conn, cur)


'''
if __name__ == '__main__':
    app = QApplication(sys.argv)

    username, no_logged = init_uname()
    playlists_metadata, playlist_picture = init_list_metadata()

    splash = SplashScreen()

    if splash.exec_() == QDialog.Accepted:
        window = Main()
        window.show()

    sys.exit(app.exec_())

'''
if __name__ == "__main__":

    username, no_logged, premium = init_uname()

    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    app = QApplication(sys.argv)
    app.setAttribute(Qt.AA_EnableHighDpiScaling)
    app.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)

    start_win = Start()

    users.remove_users(conn, cur)  # Remove deleted users if date has passed

    if not no_logged:
        playlists_metadata, playlist_picture = init_list_metadata()
        recoms, watchagain, language = init_mapping()
        splash = SplashScreen()

        if splash.exec_() == QDialog.Accepted:
            recoms, watchagain, language, random_movies = splash.movies_result
            window = Main()
            window.show()

    elif start_win.exec_() == 1:  # User registered
        checklist_win = Checklist()
        genre_win = Genre()
        lang_win = Language()

        if checklist_win.exec_() == QDialog.Accepted:
            if genre_win.exec_() == QDialog.Accepted:
                if lang_win.exec_() == QDialog.Accepted:
                    print(users.register(start_win.username, start_win.password, start_win.email, checklist_win.movies,
                                         genre_win.genres, lang_win.languages, conn, cur))
                    username, no_logged, premium = init_uname()
                    playlists_metadata, playlist_picture = init_list_metadata()
                    recoms, watchagain, language = init_mapping()
                    splash = SplashScreen()

                    if splash.exec_() == QDialog.Accepted:
                        recoms, watchagain, language, random_movies = splash.movies_result
                        window = Main()
                        window.show()

    elif start_win.exec_() == 2:  # User logged in
        username, no_logged, premium = init_uname()
        playlists_metadata, playlist_picture = init_list_metadata()
        recoms, watchagain, language = init_mapping()

        splash = SplashScreen()

        if splash.exec_() == QDialog.Accepted:
            recoms, watchagain, language, random_movies = splash.movies_result
            window = Main()
            window.show()

    sys.exit(app.exec_())
