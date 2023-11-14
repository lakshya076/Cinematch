import platform
import random
import sys
import time

from PyQt5.QtCore import Qt, QThread, QObject, pyqtSignal, QRect
from PyQt5.QtGui import QCursor, QPainter, QImage
from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi

from reusable_imports.common_vars import get_data, get_movies

# Random image for splash screen
randlist = ["one.png", "two.png", "three.png", "four.png", "five.png"]
randimg = random.choice(randlist)


class WorkerOne(QObject):
    done = pyqtSignal()

    def call(self):
        self.result = get_movies()
        print("Playlist Data Loaded")
        self.done.emit()


class WorkerTwo(QObject):
    done = pyqtSignal()

    def call(self):
        self.result = get_data()
        print("Recommendations Data Loaded, forwarding to main screen")
        self.done.emit()


class SplashScreen(QDialog):
    def __init__(self):
        super(SplashScreen, self).__init__()
        loadUi("UI\\ui_splashscreen.ui", self)

        # Checking OS
        if platform.system() == "Windows":
            print("OS check completed")
        else:
            print("This program only works on Windows systems")
            sys.exit(-2)

        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setCursor(QCursor(Qt.BlankCursor))

        self.thread = QThread(self)

        self.doing.setText("Getting Playlist Data")

        self.worker_one = WorkerOne()
        self.worker_two = WorkerTwo()

        self.worker_one.moveToThread(self.thread)
        self.worker_two.moveToThread(self.thread)

        self.thread.started.connect(self.worker_one.call)
        self.thread.started.connect(self.worker_two.call)

        self.worker_one.done.connect(self.one)
        self.worker_one.done.connect(self.worker_one.deleteLater)
        self.worker_two.done.connect(self.two)
        self.worker_two.done.connect(self.worker_two.deleteLater)

        self.thread.start()

    def one(self):
        self.progress.setValue(random.choice(range(20, 40)))
        self.doing.setText("Fetching Your Recommendations")
        time.sleep(2)

    def two(self):
        self.doing.setText("Having <i>Dahi Shakkar</i> for good luck")
        self.progress.setValue(random.choice(range(60, 85)))
        time.sleep(1)

        self.doing.setText("Manifesting 🤌🤌")
        self.progress.setValue(95)
        time.sleep(1)

        self.doing.setText("All Set")
        self.progress.setValue(100)
        time.sleep(1)
        self.movies_result = self.worker_two.result
        self.metadata_result = self.worker_one.result
        self.thread.exit()
        self.accept()

    def mousePressEvent(self, event):
        event.ignore()

    def mouseDoubleClickEvent(self, event):
        event.ignore()

    def mouseReleaseEvent(self, event):
        event.ignore()

    def mouseMoveEvent(self, event):
        event.ignore()

    def paintEvent(self, event) -> None:
        painter = QPainter(self)
        painter.drawImage(QRect(0, 0, 640, 360), QImage(f"Images/Splash/{randimg}"))
