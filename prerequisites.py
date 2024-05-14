import os
import random
import sys
from urllib.request import urlopen
import pymysql

import requests
from PyQt5.QtCore import QThread, pyqtSignal, Qt, QRect
from PyQt5.QtGui import QPainter, QImage, QCursor, QIcon
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.uic import loadUi
from cachecontrol import CacheControl
from cachecontrol.caches import FileCache

csv_url = "https://onedrive.live.com/download?resid=CE0726DF5343E9A8%21108&authkey=!ANYzCEC8y0WZf90"

cinematch_dir = f"{os.path.expanduser('~')}/AppData/Local/Cinematch"
csv_path = f"{os.path.expanduser('~')}/AppData/Local/Cinematch/csv/cos_similarity.csv"
csv_dir = f"{os.path.expanduser('~')}/AppData/Local/Cinematch/csv"

mysql_data_path = "C:/ProgramData/MySQL/MySQL Server 8.0/Data/movies"
mysql_alt_data_path = "C:/ProgramData/MySQL/MySQL Server 8.1/Data/movies"
mysql_path = "C:/Program Files/MySQL"

cache_path = f"{os.path.expanduser('~')}\\AppData\\Local\\FileCache"
session = CacheControl(requests.Session(), cache=FileCache(cache_path))
url = []
path = []

# Random image for splash screen
randlist = ["one.png", "two.png", "three.png", "four.png", "five.png"]
randimg = random.choices(randlist, weights=[0.4, 0.05, 0.2, 0.05, 0.3], k=1)  # Adding weighted random choices in splash


def get_size(file_path: str, unit: str) -> float:
    file_size = os.path.getsize(file_path)
    exponents_map = {'bytes': 0, 'kb': 1, 'mb': 2, 'gb': 3}
    if unit not in exponents_map:
        raise ValueError("Must select from ['bytes', 'kb', 'mb', 'gb']")
    else:
        size = file_size / 1024 ** exponents_map[unit]
        return round(size, 3)


def pre_check() -> int:
    if not os.path.isdir(cinematch_dir):
        os.mkdir(cinematch_dir)
        print("Directory created Cinematch")

    if not os.path.isdir(csv_dir):
        os.mkdir(csv_dir)
        print("Directory created CSV")

    if not os.path.isfile(csv_path) or get_size(csv_path, "gb") < 1.25:
        try:
            os.remove(csv_path)
        except OSError:
            pass

        url.append(csv_url)
        path.append(csv_path)
        print("To Download: CSV File")
    else:
        print("CSV is already downloaded")

    # Checking MySQL installation
    if not os.path.isdir(mysql_path):
        print("MySQL not installed. Install it before running the program")
        return 1
    elif True not in [i[:14] == "MySQL Server 8" for i in os.listdir(mysql_path)]:
        print("MySQL installation is corrupted. Install it before running the program.")
        # Open Webpage here to guide the user through the installation process
        return 1
    else:
        print("MySQL installed")

    # Checking MySQL Data
    if not (os.path.isdir(mysql_data_path) or os.path.isdir(mysql_alt_data_path)):
        try:
            os.remove(mysql_data_path)
        except OSError:
            pass
        # Open webpage here to guide the user on how to run the movies.sql file
        return 2

    else:
        print("MySQL Data Exists")

    return 0


class Downloader(QThread):
    # Signal for the window to establish the maximum value
    # of the progress bar.
    setTotalProgress = pyqtSignal(int)
    # Signal to increase the progress.
    setCurrentProgress = pyqtSignal(int)
    # Signal to be emitted when the file has been downloaded successfully.
    succeeded = pyqtSignal()

    def __init__(self, url: list, filename: list):
        super().__init__()
        self._url = url
        self._filename = filename

    def run(self):
        readBytes = 0
        chunkSize = 1024
        # Open the URL address.
        if len(url) == len(path):
            for i in range(len(self._url)):
                with urlopen(self._url[i]) as r:
                    # Tell the window the amount of bytes to be downloaded.
                    self.setTotalProgress.emit(int(r.info()["Content-Length"]))
                    with open(self._filename[i], "wb") as f:
                        while True:
                            # Read a piece of the file we are downloading.
                            chunk = r.read(chunkSize)
                            # If the result is `None`, that means data is not
                            # downloaded yet. Just keep waiting.
                            if chunk is None:
                                continue
                            # If the result is an empty `bytes` instance, then
                            # the file is complete.
                            elif chunk == b"":
                                break
                            # Write into the local file the downloaded chunk.
                            f.write(chunk)
                            readBytes += chunkSize
                            # Tell the window how many bytes we have received.
                            self.setCurrentProgress.emit(readBytes)

            self.succeeded.emit()


class Prerequisite(QDialog):
    def __init__(self):
        super(Prerequisite, self).__init__()
        loadUi("UI\\ui_pre.ui", self)

        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setCursor(QCursor(Qt.BlankCursor))
        self.setWindowTitle("Downloading Cinematch Prerequisites")
        self.setWindowIcon(QIcon("Icons/logo.png"))

        self.code = pre_check()

        self.doing.setText("Downloading prerequisites...")

        # Run the download in a new thread.
        self.downloader_thread = Downloader(url, path)

        self.downloader_thread.setTotalProgress.connect(self.progress.setMaximum)
        self.downloader_thread.setCurrentProgress.connect(self.progress.setValue)

        self.downloader_thread.succeeded.connect(self.download_succeeded)
        self.downloader_thread.finished.connect(self.download_finished)
        self.downloader_thread.start()

    def download_succeeded(self):
        # Set the progress at 100%.
        self.progress.setValue(self.progress.maximum())
        self.doing.setText("Opening Startup")

    def download_finished(self):
        del self.downloader_thread

        if self.code == 1:
            print("MySQL not installed")
            sys.exit(-3)
        elif self.code == 2:
            print("Please install the database.")
            sys.exit(-4)
        else:
            self.accept()

    def reject(self):
        pass

    def closeEvent(self, a0):
        pass

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
        painter.drawImage(QRect(0, 0, 640, 360), QImage(f"Images/Splash/{randimg[0]}"))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Prerequisite()
    print(url, path)
    window.show()
    app.exec()
