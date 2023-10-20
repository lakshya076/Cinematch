import PyQt5
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QCursor, QPixmap, QImage, QIcon
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QFrame, QPushButton

from reusable_imports.common_vars import get_playlist_movies, playlists_metadata, iso_639_1
from reusable_imports.commons import ClickableLabel, ClickableFrame

frame_style = """
    font:14pt;
    background-color: #111111; 
    color: #fffaf0;
    border-radius: 10px;
    border: 1px solid #111111;
"""


class DisplayMovies(QFrame):
    def __init__(self, playlist: str = None):
        super(DisplayMovies, self).__init__()
        self.check = get_playlist_movies(playlist)

    def new_movies_display(self, name: str, image: bytearray, title: str, lang: str, pop: str,
                           scroll_area: PyQt5.QtWidgets.QScrollArea, layout: PyQt5.QtWidgets.QVBoxLayout,
                           open_movie=None, delete_movie=None):
        # unique identifiers for each frame,image,title
        self.frame_new = f"movie_frame_{name}"
        self.image_new = f"movie_image_{name}"
        self.title_new = f"movie_title_{name}"
        self.lang_new = f"movie_lang_{name}"
        self.pop_new = f"movie_pop_{name}"
        self.movie_delete_new = f"movie_delete_{name}"

        self.movie_frame = ClickableFrame(scroll_area)
        self.movie_frame.setObjectName(self.frame_new)
        self.movie_frame.setStyleSheet(frame_style)
        self.movie_frame.setMaximumHeight(125)
        setattr(self, self.frame_new, self.movie_frame)

        self.image = ClickableLabel(self.movie_frame)
        self.image.setObjectName(self.image_new)
        self.image.setFixedSize(QSize(60, 90))
        self.image.setScaledContents(True)
        image_object = QImage()
        image_object.loadFromData(image)
        self.image.setPixmap(QPixmap(image_object))
        setattr(self, self.image_new, self.image)

        self.title = ClickableLabel(self.movie_frame)
        self.title.setObjectName(self.title_new)
        self.title.setMinimumSize(QSize(0, 50))
        self.title.setMaximumSize(QSize(16777215, 50))
        self.title.setText(title)
        setattr(self, self.title_new, self.title)

        self.lang = ClickableLabel(self.movie_frame)
        self.lang.setObjectName(self.lang_new)
        self.lang.setMinimumSize(QSize(100, 50))
        self.lang.setMaximumSize(QSize(100, 50))
        try:
            try:
                lang = iso_639_1[lang].split(sep=";")[0].strip()
            except:
                lang = iso_639_1[lang]

            self.lang.setText(lang)
        except KeyError:
            self.lang.setText(lang)
        setattr(self, self.lang_new, self.lang)

        self.pop = ClickableLabel(self.movie_frame)
        self.pop.setObjectName(self.pop_new)
        self.pop.setFixedSize(QSize(70, 50))
        self.pop.setStyleSheet("font:10pt;")
        self.pop.setText(str(pop))
        setattr(self, self.pop_new, self.pop)

        self.movie_delete = QPushButton(self.movie_frame)
        self.movie_delete.setObjectName(self.movie_delete_new)
        self.movie_delete.setIconSize(QSize(24, 24))
        self.movie_delete.setFixedSize(QSize(32, 32))
        self.movie_delete.setIcon(QIcon("Icons\\delete.ico"))
        self.movie_delete.setToolTip(f"Delete movie from {playlists_metadata[self.frame_new.split(sep='_')[-2]][0]}")
        self.movie_delete.setCursor(QCursor(Qt.PointingHandCursor))
        setattr(self, self.movie_delete_new, self.movie_delete)

        self.movie_frame_hlayout = QHBoxLayout(self.movie_frame)
        self.movie_frame_hlayout.setObjectName(u"movie_frame_hlayout")
        self.movie_frame_hlayout.setSpacing(9)

        self.movie_frame_hlayout.addWidget(self.image)
        self.movie_frame_hlayout.addWidget(self.title)
        self.movie_frame_hlayout.addWidget(self.lang)
        self.movie_frame_hlayout.addWidget(self.pop)
        self.movie_frame_hlayout.addWidget(self.movie_delete)

        layout.addWidget(self.movie_frame)

        self.movie_frame.clicked.connect(lambda: open_movie())
        self.image.clicked.connect(lambda: open_movie())
        self.title.clicked.connect(lambda: open_movie())
        self.lang.clicked.connect(lambda: open_movie())
        self.pop.clicked.connect(lambda: open_movie())
        self.movie_delete.clicked.connect(lambda: delete_movie())
