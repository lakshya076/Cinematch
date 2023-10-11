from PySide2 import QtCore, QtWidgets


class Dialog(QtWidgets.QDialog):
    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        if event.button() == QtCore.Qt.LeftButton:
            p = self.mapToGlobal(event.pos())
            menu = self.create_menu_contextual()
            action = menu.exec_(p)
            if action is not None:
                print(action.text())

    def create_menu_contextual(self):
        menu = QtWidgets.QMenu()
        menu.addAction("Action1")
        menu.addAction("Action2")
        return menu


def main():
    import sys

    app = QtWidgets.QApplication(sys.argv)
    w = Dialog()
    w.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
