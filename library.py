import PyQt5
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QCursor, QPixmap, QIcon
from PyQt5.QtWidgets import QMenu, QPushButton, QHBoxLayout, QSpacerItem, QSizePolicy, QVBoxLayout, QFrame

from reusable_imports._css import dark_library_stylesheet
from reusable_imports.commons import ClickableLabel, ClickableFrame


class Library(QFrame):
    """
    Class to show playlist covers in the library page of main window
    """

    def __init__(self):
        super(Library, self).__init__()

    def new_widgets_lib(self, name: str, row: int, column: int, display_name: str, _username: str, dob: str, image: str,
                        scroll_area: PyQt5.QtWidgets.QScrollArea, layout: PyQt5.QtWidgets.QGridLayout,
                        delete_func_lib=None, open_func_lib=None):
        """
        function to add new widgets to the library page of main window
        """
        # unique identifiers
        self.frame_new = f"frame_{name}"
        self.poster_new = f"poster_{name}"
        self.title_new = f"title_{name}"
        self.add_new = f"add_{name}"
        self.delete_playlist_new = f"delete_playlist_{name}"
        self.user_new = f"user_{name}"
        self.dob_new = f"dob_{name}"

        self.frame = ClickableFrame(scroll_area)
        self.frame.setObjectName(self.frame_new)
        self.frame.setFixedSize(QSize(200, 250))
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.frame.setStyleSheet(dark_library_stylesheet)
        setattr(self, self.frame_new, self.frame)

        self.poster = ClickableLabel(self.frame)
        self.poster.setObjectName(self.poster_new)
        self.poster.setScaledContents(True)
        self.poster.setPixmap(QPixmap(image))
        setattr(self, self.poster_new, self.poster)

        self.title = ClickableLabel(self.frame)
        self.title.setObjectName(self.title_new)
        self.title.setText(display_name)
        self.title.setFixedHeight(30)
        self.title.setStyleSheet(u"font:15pt;")
        self.title.setScaledContents(True)
        setattr(self, self.title_new, self.title)

        self.verticalspacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.delete_playlist = QPushButton(self.frame)
        self.delete_playlist.setObjectName(self.delete_playlist_new)
        self.delete_playlist.setFixedSize(QSize(32, 32))
        self.delete_playlist.setIconSize(QSize(24, 24))
        self.delete_playlist.setIcon(QIcon("Icons/delete.ico"))
        self.delete_playlist.setToolTip(f"Delete {display_name}")
        self.delete_playlist.setCursor(QCursor(Qt.PointingHandCursor))
        setattr(self, self.delete_playlist_new, self.delete_playlist)

        self.user = ClickableLabel(self.frame)
        self.user.setObjectName(self.user_new)
        self.user.setStyleSheet(u"font:12pt;")
        self.user.setAlignment(Qt.AlignRight)
        self.user.setText(_username)
        self.user.setWordWrap(True)
        setattr(self, self.user_new, self.user)

        self.dob = ClickableLabel(self.frame)
        self.dob.setObjectName(self.dob_new)
        self.dob.setStyleSheet(u"font:8pt;")
        self.dob.setAlignment(Qt.AlignRight)
        self.dob.setText(dob)
        setattr(self, self.dob_new, self.dob)

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

        self.title_delete_hlayout = QHBoxLayout()
        self.title_delete_hlayout.addWidget(self.title)
        self.title_delete_hlayout.addWidget(self.delete_playlist)

        self.poster_button_hlayout.addWidget(self.poster)

        self.frame_vlayout_library.addLayout(self.poster_button_hlayout)
        self.frame_vlayout_library.addLayout(self.title_delete_hlayout)
        self.frame_vlayout_library.addWidget(self.user)
        self.frame_vlayout_library.addWidget(self.dob)

        layout.addWidget(self.frame, row, column, Qt.AlignHCenter | Qt.AlignVCenter)
