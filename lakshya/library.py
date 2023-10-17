import PyQt5
from PyQt5.QtCore import Qt, QSize, QEvent
from PyQt5.QtGui import QCursor, QPixmap, QIcon
from PyQt5.QtWidgets import QMenu, QPushButton, QHBoxLayout, QSpacerItem, QSizePolicy, QLabel, QVBoxLayout, QFrame

from reusable_imports.commons import clickable
from reusable_imports._css import dark_menu, dark_library_stylesheet

_obj_library = ""


class LibraryButton(QPushButton):
    def __init__(self, parent=None):
        super(LibraryButton, self).__init__(parent)

        self.setFixedSize(QSize(32, 32))
        self.setIconSize(QSize(32, 32))
        self.setIcon(QIcon("Icons\\kebab_white.png"))
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.setToolTip("Manage Playlist")

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        if event.button() == Qt.LeftButton:
            print(self.objectName())
            position = self.mapToGlobal(event.pos())
            menu = self.create_menu_contextual()
            action = menu.exec_(position)

            if action is not None:
                _type = str(action.text()).strip().split()
                if _type[0] == "Manage":
                    self.divert_manage()
                elif _type[0] == "Open":
                    self.divert_open()
                elif _type[0] == "Add":
                    self.divert_add()
                elif _type[0] == "Delete":
                    self.divert_delete()

    def create_menu_contextual(self):
        menu = QMenu()
        menu.addAction("Manage Playlist")
        menu.addAction("Open Playlist")
        menu.addAction("Add to Playlist")
        menu.addAction("Delete Playlist")
        menu.setStyleSheet(dark_menu)
        return menu

    def divert_manage(self):
        print("Manage")

    def divert_open(self):
        print(f"Opening playlist {self.objectName().split(sep='_')[1]}")

    def divert_add(self):
        print("Add")

    def divert_delete(self):
        _object = self.objectName().strip().split(sep="_")
        if _object[1].lower() in ["shortlisted"]:
            print("Can't Delete Pre-Built Playlist")
        else:
            print("Playlist Deleted")


class LibraryLabel(QLabel):
    def __init__(self, parent=None):
        super(LibraryLabel, self).__init__(parent)
        self.installEventFilter(self)

    def eventFilter(self, source, event):
        if event.type() == QEvent.MouseButtonPress:
            global _obj_library
            _obj_library = source.objectName()
            _obj_library = _obj_library.split(sep="_")[1]

        return super().eventFilter(source, event)


class Library(QFrame):
    def __init__(self):
        super(Library, self).__init__()

        global _obj_library

    def new_widgets_lib(self, name: str, row: int, column: int, display_name: str, _username: str, dob: str, image: str,
                        scroll_area: PyQt5.QtWidgets.QScrollArea, layout: PyQt5.QtWidgets.QGridLayout):
        # unique identifiers for each frame,image,title
        self.frame_new = f"frame_{name}"
        self.poster_new = f"poster_{name}"
        self.title_new = f"title_{name}"
        self.manage_new = f"manage_{name}"
        self.add_new = f"add_{name}"
        self.deletelist_new = f"deletelist_{name}"
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

        self.manage = LibraryButton(self.frame)
        self.manage.setObjectName(self.manage_new)
        setattr(self, self.manage_new, self.manage)

        self.add = QPushButton(self.frame)
        self.add.setObjectName(self.add_new)
        self.add.setFixedSize(QSize(32, 32))
        self.add.setIconSize(QSize(24, 24))
        self.add.setIcon(QIcon("Icons\\add.ico"))
        self.add.setCursor(QCursor(Qt.PointingHandCursor))
        self.add.setToolTip("Add to Playlist")
        setattr(self, self.add_new, self.add)

        self.verticalspacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.deletelist = QPushButton(self.frame)
        self.deletelist.setObjectName(self.deletelist_new)
        self.deletelist.setFixedSize(QSize(32, 32))
        self.deletelist.setIconSize(QSize(24, 24))
        self.deletelist.setIcon(QIcon("Icons\\delete.ico"))
        self.deletelist.setCursor(QCursor(Qt.PointingHandCursor))
        self.deletelist.setToolTip("Delete Playlist")
        setattr(self, self.deletelist_new, self.deletelist)

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

        self.add.clicked.connect(lambda: self.add_playlist())
        self.deletelist.clicked.connect(lambda: self.delete_playlist())
        clickable(self.poster).connect(self.open_playlist)
        clickable(self.title).connect(self.open_playlist)
        clickable(self.user).connect(self.open_playlist)
        clickable(self.dob).connect(self.open_playlist)

        # Setting Layouts
        self.frame_vlayout_library = QVBoxLayout(self.frame)
        self.frame_vlayout_library.setObjectName(u"frame_vlayout_library")

        self.poster_button_hlayout = QHBoxLayout()
        self.poster_button_hlayout.setObjectName(u"poster_button_hlayout")

        self.button_vlayout = QVBoxLayout()
        self.button_vlayout.setObjectName(u"button_vlayout")
        self.button_vlayout.addWidget(self.manage)
        self.button_vlayout.addWidget(self.add)
        self.button_vlayout.addWidget(self.deletelist)
        self.button_vlayout.addItem(self.verticalspacer)

        self.poster_button_hlayout.addWidget(self.poster)
        self.poster_button_hlayout.addLayout(self.button_vlayout)

        self.frame_vlayout_library.addLayout(self.poster_button_hlayout)
        self.frame_vlayout_library.addWidget(self.title)
        self.frame_vlayout_library.addWidget(self.user)
        self.frame_vlayout_library.addWidget(self.dob)

        layout.addWidget(self.frame, row, column, Qt.AlignHCenter | Qt.AlignVCenter)

    def add_playlist(self):
        print("Add to playlist")

    def delete_playlist(self):
        sender = self.sender()
        _object = sender.objectName().strip().split(sep="_")
        if _object[1].lower() in ["shortlisted"]:
            print("Can't Delete Pre-Built Playlist")
        else:
            print("Playlist Deleted")

    def open_playlist(self):
        print(f"Opening Playlist {_obj_library}")
