from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QLabel


# Modifying QLabel class for displaying add button in shortlist window
class ShortListLabel(QLabel):
    clicked = pyqtSignal()

    def __init__(self, parent=None):
        super(ShortListLabel, self).__init__(parent)
        self.setCursor(QCursor(Qt.PointingHandCursor))

    def mousePressEvent(self, QMouseEvent):
        self.clicked.emit()
