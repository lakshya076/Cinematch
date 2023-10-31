import random
import sys
import time

from PyQt5.QtCore import Qt, QThread, QObject, pyqtSignal
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow
from PyQt5.uic import loadUi

from reusable_imports.common_vars import get_data, get_movies


class WorkerOne(QObject):
    done = pyqtSignal()

    def call(self):
        get_movies()
        self.done.emit()


class WorkerTwo(QObject):
    done = pyqtSignal()

    def call(self):
        get_data()
        self.done.emit()


class SplashScreen(QDialog):
    def __init__(self):
        super(SplashScreen, self).__init__()
        loadUi("UI\\ui_splashscreen.ui", self)

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
        self.accept()

    def mousePressEvent(self, event):
        event.ignore()

    def mouseDoubleClickEvent(self, event):
        event.ignore()

    def mouseReleaseEvent(self, event):
        event.ignore()

    def mouseMoveEvent(self, event):
        event.ignore()
