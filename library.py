import PyQt5
from PyQt5.QtCore import Qt, QSize, pyqtSignal
from PyQt5.QtGui import QCursor, QPixmap, QIcon
from PyQt5.QtWidgets import QMenu, QPushButton, QHBoxLayout, QSpacerItem, QSizePolicy, QLabel, QVBoxLayout, QFrame

from reusable_imports._css import dark_library_stylesheet

_obj_library = ""


class LibraryLabel(QLabel):
    clicked = pyqtSignal()

    def __init__(self, parent=None):
        super(LibraryLabel, self).__init__(parent)

    def mousePressEvent(self, QMouseEvent):
        self.clicked.emit()

        global _obj_library
        _obj_library = self.objectName()
        _obj_library = _obj_library.split(sep="_")[1]


class Library(QFrame):
    def __init__(self):
        super(Library, self).__init__()

        global _obj_library

    def new_widgets_lib(self, name: str, row: int, column: int, display_name: str, _username: str, dob: str, image: str,
                        scroll_area: PyQt5.QtWidgets.QScrollArea, layout: PyQt5.QtWidgets.QGridLayout,
                        add_func_lib=None, delete_func_lib=None, open_func_lib=None):
        # unique identifiers for each frame,image,title
        self.frame_new = f"frame_{name}"
        self.poster_new = f"poster_{name}"
        self.title_new = f"title_{name}"
        self.add_new = f"add_{name}"
        self.delete_playlist_new = f"delete_playlist_{name}"
        self.user_new = f"user_{name}"
        self.dob_new = f"dob_{name}"
        print(self.frame_new)

        self.frame = QFrame(scroll_area)
        self.frame.setObjectName(self.frame_new)
        self.frame.setFixedSize(QSize(200, 250))
        self.frame.setContentsMargins(0, 0, 0, 0)
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.frame.setCursor(QCursor(Qt.PointingHandCursor))
        self.frame.setStyleSheet(dark_library_stylesheet)
        setattr(self, self.frame_new, self.frame)

        self.poster = LibraryLabel(self.frame)
        self.poster.setObjectName(self.poster_new)
        self.poster.setText("Image")
        self.poster.setCursor(QCursor(Qt.PointingHandCursor))
        self.poster.setPixmap(QPixmap(image))
        setattr(self, self.poster_new, self.poster)

        self.title = LibraryLabel(self.frame)
        self.title.setObjectName(self.title_new)
        self.title.setText(display_name)
        self.title.setFixedHeight(30)
        self.title.setStyleSheet(u"font:15pt;")
        self.title.setScaledContents(True)
        self.title.setWordWrap(True)
        self.title.setCursor(QCursor(Qt.PointingHandCursor))
        setattr(self, self.title_new, self.title)

        self.add = QPushButton(self.frame)
        self.add.setObjectName(self.add_new)
        self.add.setFixedSize(QSize(32, 32))
        self.add.setIconSize(QSize(24, 24))
        self.add.setIcon(QIcon("Icons/add.ico"))
        self.add.setToolTip(f"Add to {display_name}")
        self.add.setCursor(QCursor(Qt.PointingHandCursor))
        setattr(self, self.add_new, self.add)

        self.verticalspacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.delete_playlist = QPushButton(self.frame)
        self.delete_playlist.setObjectName(self.delete_playlist_new)
        self.delete_playlist.setFixedSize(QSize(32, 32))
        self.delete_playlist.setIconSize(QSize(24, 24))
        self.delete_playlist.setIcon(QIcon("Icons/delete.ico"))
        self.delete_playlist.setToolTip(f"Delete {display_name}")
        self.delete_playlist.setCursor(QCursor(Qt.PointingHandCursor))
        setattr(self, self.delete_playlist_new, self.delete_playlist)

        self.user = LibraryLabel(self.frame)
        self.user.setObjectName(self.user_new)
        self.user.setStyleSheet(u"font:12pt;")
        self.user.setAlignment(Qt.AlignRight)
        self.user.setText(_username)
        self.user.setWordWrap(True)
        self.user.setCursor(QCursor(Qt.PointingHandCursor))
        setattr(self, self.user_new, self.user)

        self.dob = LibraryLabel(self.frame)
        self.dob.setObjectName(self.dob_new)
        self.dob.setStyleSheet(u"font:8pt;")
        self.dob.setAlignment(Qt.AlignRight)
        self.dob.setText(dob)
        self.dob.setCursor(QCursor(Qt.PointingHandCursor))
        setattr(self, self.dob_new, self.dob)

        self.add.clicked.connect(lambda: add_func_lib())
        self.delete_playlist.clicked.connect(lambda: delete_func_lib())
        self.poster.clicked.connect(lambda: open_func_lib())
        self.title.clicked.connect(lambda: open_func_lib())
        self.user.clicked.connect(lambda: open_func_lib())
        self.dob.clicked.connect(lambda: open_func_lib())

        # Setting Layouts
        self.frame_vlayout_library = QVBoxLayout(self.frame)
        self.frame_vlayout_library.setObjectName(u"frame_vlayout_library")

        self.poster_button_hlayout = QHBoxLayout()
        self.poster_button_hlayout.setObjectName(u"poster_button_hlayout")

        self.button_vlayout = QVBoxLayout()
        self.button_vlayout.setObjectName(u"button_vlayout")
        self.button_vlayout.addWidget(self.add)
        self.button_vlayout.addWidget(self.delete_playlist)
        self.button_vlayout.addItem(self.verticalspacer)

        self.poster_button_hlayout.addWidget(self.poster)
        self.poster_button_hlayout.addLayout(self.button_vlayout)

        self.frame_vlayout_library.addLayout(self.poster_button_hlayout)
        self.frame_vlayout_library.addWidget(self.title)
        self.frame_vlayout_library.addWidget(self.user)
        self.frame_vlayout_library.addWidget(self.dob)

        layout.addWidget(self.frame, row, column, Qt.AlignHCenter | Qt.AlignVCenter)
