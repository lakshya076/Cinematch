import random
import sys
import time
from threading import Thread

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.uic import loadUi

from reusable_imports.common_vars import get_data, get_movies


class SplashScreen(QDialog):
    def __init__(self):
        super(SplashScreen, self).__init__()
        loadUi("UI\\ui_splashscreen.ui", self)

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setCursor(QCursor(Qt.BlankCursor))

        self.timer = QTimer()
        self.timer.timeout.connect(self.call)
        self.timer.start(30)

        self.doing.setText("Getting playlist data")

    def call(self):
        self.doing.setText("Getting your recommendations")
        _thread = Thread(target=get_movies)
        _thread.start()
        _thread.join()
        self.progress.setValue(random.choice(range(20, 40)))

        self.doing.setText("Adding a pinch of salt for good luck")
        _thread_2 = Thread(target=get_data)
        _thread_2.start()
        _thread_2.join()
        self.progress.setValue(random.choice(range(75, 85)))

        self.doing.setText("Manifesting")
        time.sleep(1)
        self.progress.setValue(random.choice(range(85, 95)))

        self.doing.setText("All Set")
        time.sleep(2)
        self.progress.setValue(100)
        time.sleep(2)

        self.accept()

    def mousePressEvent(self, event):
        event.ignore()

    def mouseDoubleClickEvent(self, event):
        event.ignore()

    def mouseReleaseEvent(self, event):
        event.ignore()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = SplashScreen()
    window.show()
    sys.exit(app.exec_())
