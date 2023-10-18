from PyQt5.QtCore import QEvent, pyqtSignal, QObject, Qt
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QMessageBox, QLabel, QFrame


class ClickableLabel(QLabel):
    clicked = pyqtSignal()

    def __init__(self, parent=None):
        super(ClickableLabel, self).__init__(parent)
        self.setCursor(QCursor(Qt.PointingHandCursor))

    def mousePressEvent(self, QMouseEvent):
        self.clicked.emit()


class ClickableFrame(QFrame):
    clicked = pyqtSignal()

    def __init__(self, parent=None):
        super(ClickableFrame, self).__init__(parent)
        self.setCursor(QCursor(Qt.PointingHandCursor))

    def mousePressEvent(self, QMouseEvent):
        self.clicked.emit()


def clickable(widget):
    """
    Helps to detect the event in which a non-clickable widget (Ex - Label) is clicked by using the Mouse Button Release
    QEvent. A signal is emitted upon clicking the widget on which this function is used. That signal can be relayed to
    the program and the click (mouse release) event can be used.
    :param: widget
    :return: Bool
    """

    class Filter(QObject):
        clicked = pyqtSignal()

        def eventFilter(self, obj, event):
            if obj == widget:
                if event.type() == QEvent.MouseButtonRelease:
                    if obj.rect().contains(event.pos()):
                        self.clicked.emit()
                        return True
            return False

    _filter = Filter(widget)
    widget.installEventFilter(_filter)
    return _filter.clicked


class ErrorDialog(QMessageBox):
    """
    generic reusable code to display an error dialog box
    """

    def __init__(self):
        super(ErrorDialog, self).__init__()

        self.error_dialog = QMessageBox(self)
        self.error_dialog.setWindowTitle("")
        self.error_dialog.setText("")
        self.error_dialog.button(QMessageBox.Ok)
        self.error_dialog.setDefaultButton(QMessageBox.Ok)
        self.error_dialog.setStyleSheet("background-color: #FFFAF0; font: 10pt\"MS Shell Dlg 2\";")
        self.error_dialog.setIcon(QMessageBox.Warning)
