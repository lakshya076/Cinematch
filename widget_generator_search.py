import PyQt5

from PyQt5.QtCore import QSize
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QMenu, QVBoxLayout, QFrame

from reusable_imports.commons import ClickableLabel, ClickableFrame


class SearchMovies(QFrame):
    def __init__(self):
        super(SearchMovies, self).__init__()

    def new_widgets_search(self, id: int, title: str, image: bytes, scroll_area: PyQt5.QtWidgets.QScrollArea,
                           layout: PyQt5.QtWidgets.QHBoxLayout, open_func_lib=None):
        """
        function to create widgets and display it in the search screen
        """
        # unique identifiers for each frame,image,title
        self.frame_new = f"frame_search_{id}"
        self.poster_new = f"poster_search_{id}"
        self.title_new = f"title_search_{id}"

        self.frame = ClickableFrame(scroll_area)
        self.frame.setObjectName(self.frame_new)
        self.frame.setFixedSize(QSize(200, 375))
        setattr(self, self.frame_new, self.frame)

        self.poster = ClickableLabel(self.frame)
        self.poster.setObjectName(self.poster_new)
        self.poster.setScaledContents(True)
        self.poster.setFixedSize(QSize(180, 270))
        image_object = QImage()
        image_object.loadFromData(image)
        _image = QPixmap(image_object)
        self.poster.setPixmap(QPixmap(_image))
        setattr(self, self.poster_new, self.poster)

        self.title = ClickableLabel(self.frame)
        self.title.setObjectName(self.title_new)
        self.title.setText(title)
        self.title.setStyleSheet(u"font:10pt;")
        self.title.setWordWrap(True)
        setattr(self, self.title_new, self.title)

        self.frame.clicked.connect(lambda: open_func_lib())
        self.poster.clicked.connect(lambda: open_func_lib())
        self.title.clicked.connect(lambda: open_func_lib())

        # Setting Layouts
        self.frame_vlayout_search = QVBoxLayout(self.frame)
        self.frame_vlayout_search.setObjectName(u"frame_vlayout_search")

        self.frame_vlayout_search.addWidget(self.poster)
        self.frame_vlayout_search.addWidget(self.title)

        layout.addWidget(self.frame)
