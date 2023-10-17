import PyQt5
from PyQt5.QtCore import Qt, QSize, QEvent
from PyQt5.QtGui import QCursor, QPixmap, QImage, QIcon
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QLabel, QFrame, QPushButton, QMenu
from PyQt5.uic import loadUi

from reusable_imports._css import dark_menu
from reusable_imports.common_vars import get_movies, get_playlist_movies, playlists_metadata
from reusable_imports.commons import clickable

_obj_lists = ""
frame_style = """
    font:14pt; 
    background-color: #111111; 
    color: #fffaf0; 
    border-radius: 10px; 
    border: 1px solid #111111;
"""


class MovieButton(QPushButton):
    def __init__(self, parent=None, name: str = None):
        super(MovieButton, self).__init__(parent)

        self.setIconSize(QSize(32, 32))
        self.setFixedSize(QSize(32, 32))
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.setIcon(QIcon("Icons/kebab_white.png"))
        self.setStyleSheet("border: none; background_color: rgba(0,0,0,0); font: 10pt;")
        self.setToolTip("Manage Playlist")

        _object = name.strip().split(sep="_")
        self.movie_id = _object[-1]
        self.playlist_name = _object[-2]

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        if event.button() == Qt.LeftButton:
            position = self.mapToGlobal(event.pos())
            menu = self.create_menu_contextual()
            action = menu.exec_(position)

            if action is not None:
                _type = str(action.text()).strip().split()
                if _type[-1] == "Shortlist" and _type[0] == "Add":
                    self.add_to_shortlist()
                elif _type[0] == "Open":
                    self.divert_open()
                elif _type[0] == "Add":
                    self.divert_add()
                elif _type[0] == "Remove":
                    self.diver_remove()

    def create_menu_contextual(self):
        menu = QMenu()
        menu.addAction("Add to Shortlist")
        menu.addAction("Open Movie")
        menu.addAction(f"Add to another playlist")  # redirect to add to playlist page with the selected movie open
        menu.addAction(f"Remove from {playlists_metadata[self.playlist_name][0]}")
        menu.setStyleSheet(dark_menu)
        return menu

    def add_to_shortlist(self):
        if self.playlist_name == "shortlist":
            print("Movie already in shortlist")
        else:
            print(f"Adding {self.movie_id} to shortlist")

    def divert_open(self):
        print(f"Opening movie {self.movie_id} in {self.playlist_name.title()}")

    def divert_add(self):
        print(f"Adding {self.movie_id}")
        # create sub menu

    def diver_remove(self):
        print(f"Deleted movie {self.movie_id} from playlist {self.playlist_name.title()}")


class MovieLabel(QLabel):
    def __init__(self, parent=None):
        super(MovieLabel, self).__init__(parent)
        self.installEventFilter(self)

    def eventFilter(self, source, event):
        if event.type() == QEvent.MouseButtonPress:
            global _obj_lists
            _obj_lists = source.objectName()
            _obj_lists = str(_obj_lists.split(sep="_")[-1])
            print(f"Clicked {_obj_lists}")

        return super().eventFilter(source, event)


class DisplayMovies(QFrame):
    def __init__(self, playlist: str = None):
        super(DisplayMovies, self).__init__()
        self.check = get_playlist_movies(playlist)

        global _obj_lists

    def new_movies_display(self, name: str, image: bytearray, title: str, lang: str, pop: str,
                           scroll_area: PyQt5.QtWidgets.QScrollArea, layout: PyQt5.QtWidgets.QVBoxLayout):
        # unique identifiers for each frame,image,title
        self.frame_new = f"movie_frame_{name}"
        self.image_new = f"movie_image_{name}"
        self.title_new = f"movie_title_{name}"
        self.lang_new = f"movie_lang_{name}"
        self.pop_new = f"movie_pop_{name}"
        self.movie_manage_new = f"movie_manage_{name}"
        print(self.frame_new)

        self.movie_frame = QFrame(scroll_area)
        self.movie_frame.setObjectName(self.frame_new)
        self.movie_frame.setStyleSheet(frame_style)
        setattr(self, self.frame_new, self.movie_frame)

        self.image = MovieLabel(self.movie_frame)
        self.image.setObjectName(self.image_new)
        self.image.setFixedSize(QSize(50, 75))
        self.image.setScaledContents(True)
        image_object = QImage()
        image_object.loadFromData(image)
        self.image.setPixmap(QPixmap(image_object))
        self.image.setCursor(QCursor(Qt.PointingHandCursor))
        setattr(self, self.image_new, self.image)

        self.title = MovieLabel(self.movie_frame)
        self.title.setObjectName(self.title_new)
        self.title.setMinimumSize(QSize(0, 50))
        self.title.setMaximumSize(QSize(16777215, 50))
        self.title.setText(title)
        self.title.setCursor(QCursor(Qt.PointingHandCursor))
        setattr(self, self.title_new, self.title)

        self.lang = MovieLabel(self.movie_frame)
        self.lang.setObjectName(self.lang_new)
        self.lang.setMinimumSize(QSize(50, 50))
        self.lang.setMaximumSize(QSize(50, 50))
        self.lang.setText(lang)
        self.lang.setCursor(QCursor(Qt.PointingHandCursor))
        setattr(self, self.lang_new, self.lang)

        self.pop = MovieLabel(self.movie_frame)
        self.pop.setObjectName(self.pop_new)
        self.pop.setFixedSize(QSize(70, 50))
        self.pop.setStyleSheet("font:10pt;")
        self.pop.setText(str(pop))
        self.pop.setCursor(QCursor(Qt.PointingHandCursor))
        setattr(self, self.pop_new, self.pop)

        self.movie_manage = MovieButton(self.movie_frame, self.movie_manage_new)
        self.movie_manage.setObjectName(self.movie_manage_new)
        setattr(self, self.movie_manage_new, self.movie_manage)

        self.movie_frame_hlayout = QHBoxLayout(self.movie_frame)
        self.movie_frame_hlayout.setObjectName(u"movie_frame_hlayout")
        self.movie_frame_hlayout.setSpacing(9)

        self.movie_frame_hlayout.addWidget(self.image)
        self.movie_frame_hlayout.addWidget(self.title)
        self.movie_frame_hlayout.addWidget(self.lang)
        self.movie_frame_hlayout.addWidget(self.pop)
        self.movie_frame_hlayout.addWidget(self.movie_manage)

        layout.addWidget(self.movie_frame)

        clickable(self.image).connect(self.open_movie)
        clickable(self.title).connect(self.open_movie)
        clickable(self.lang).connect(self.open_movie)
        clickable(self.pop).connect(self.open_movie)

    def open_movie(self):
        print(f"Opening movie {_obj_lists}")
