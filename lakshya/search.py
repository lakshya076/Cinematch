from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QLineEdit


# Modified QLineEdit class for the search bar
# Adding the clicked signal which is slotted within main.py
# Text gets selected when text box is clicked
class Search(QLineEdit):
    clicked = pyqtSignal()

    def __init__(self, parent=None):
        super(Search, self).__init__(parent)

    def mousePressEvent(self, QMouseEvent):
        self.clicked.emit()
        self.selectAll()
