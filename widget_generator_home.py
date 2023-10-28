import PyQt5
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QMenu, QVBoxLayout, QFrame

from reusable_imports._css import dark_home_stylesheet
from reusable_imports.commons import ClickableLabel, ClickableFrame


class Home(QFrame):
    def __init__(self):
        super(Home, self).__init__()

    def new_widgets_home(self, id: int, title: str, image: bytes, scroll_area: PyQt5.QtWidgets.QScrollArea,
                         layout: PyQt5.QtWidgets.QHBoxLayout, open_func_lib=None):
        """
        function to create widgets and display it in the home screen
        """
        # unique identifiers for each frame,image,title
        self.frame_new = f"frame_home_{id}"
        self.poster_new = f"poster_home_{id}"
        self.title_new = f"title_home_{id}"

        self.frame = ClickableFrame(scroll_area)
        self.frame.setObjectName(self.frame_new)
        self.frame.setFixedSize(QSize(168, 325))
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.frame.setStyleSheet(dark_home_stylesheet)
        setattr(self, self.frame_new, self.frame)

        self.poster = ClickableLabel(self.frame)
        self.poster.setObjectName(self.poster_new)
        self.poster.setScaledContents(True)
        self.poster.setFixedSize(QSize(150, 225))
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
        self.frame_vlayout_home = QVBoxLayout(self.frame)
        self.frame_vlayout_home.setObjectName(u"frame_vlayout_home")

        self.frame_vlayout_home.addWidget(self.poster)
        self.frame_vlayout_home.addWidget(self.title)

        layout.addWidget(self.frame)
