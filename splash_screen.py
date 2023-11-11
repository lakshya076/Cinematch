import platform
import random
import sys
import time
import pandas

from PyQt5.QtCore import Qt, QThread, QObject, pyqtSignal
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow
from PyQt5.uic import loadUi

from reusable_imports.common_vars import get_data, get_movies


class WorkerOne(QObject):
    done = pyqtSignal()

    def call(self):
        get_movies()
        self.item_similarity = pandas.read_csv('backend/cos_similarity.csv', index_col=0)
        print("File Read")
        self.done.emit()


class WorkerTwo(QObject):
    done = pyqtSignal()

    def call(self):
        self.result = get_data()
        print("Data got, loading main screen")
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
        time.sleep(2)

        self.doing.setText("Manifesting 🤌🤌")
        self.progress.setValue(95)
        time.sleep(2)

        self.doing.setText("All Set")
        self.progress.setValue(100)
        time.sleep(2)
        self.movies_result = self.worker_two.result
        self.item_similarity = self.worker_one.item_similarity
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
