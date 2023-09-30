import sys
import requests
import mysql.connector
from PyQt5.QtCore import QSize, Qt, QEvent
from PyQt5.QtGui import QCursor, QImage, QPixmap, QIcon
from PyQt5.QtWidgets import QFrame, QApplication, QLabel, QVBoxLayout, QDialog, QMessageBox, QHBoxLayout, QLayout
from PyQt5.uic import loadUi
from reusable.click import clickable

# modify according to code later in school
# to make each frame image and title unique, instead putting it in the new_widgets_search function, make a loop and
# put it in __init__ cuz new_widgets_search is a static function to regenerate the same type of widgets
# (without content) and place them in the window. It doesn't change the contents of frame.

# 168,325 : 150,225 : 150,60 -> preferred layouts of frame, image and title for the main ui page

_obj_ = ""
selected_movies_display = 0
selected_movies_search = 0
real_selected_movies_search = 0

from_db = "/qnqGbB22YJ7dSs4o6M7exTpNxPz.jpg"
url = f"https://image.tmdb.org/t/p/original{from_db}"
image = requests.get(url).content

frame_css = """
        border-radius:5px; 
        border-color:black black black black; 
        background-color:rgb(255, 231, 250); 
        selection-background-color: black; 
        border-width: 2px; 
        border-style: solid; 
        border-color: rgb(9, 23, 217) rgb(9, 23, 217) rgb(9, 23, 217) rgb(9, 23, 217);
"""

image_css = """
border-radius:0px;
background-color:rgb(255, 231, 250);
border-color:rgb(255, 231, 250) rgb(255, 231, 250) rgb(255, 231, 250) rgb(255, 231, 250);
"""

title_css = """
border-radius:0px;
background-color:rgb(255, 231, 250);
border-color:rgb(255, 231, 250) rgb(255, 231, 250) rgb(255, 231, 250) rgb(255, 231, 250);
"""

frame_true_css = """
        border-radius:10px; 
        background-color:rgb(255, 231, 250);
        """

# initiating mysql connection
conn = mysql.connector.connect(host="localhost", user="root", password="root")
cursor = conn.cursor()


class Selected(QMessageBox):
    """
    reusable code to display a dialog box in the program if the minimum threshold of selected movies (i.e. 5) is not met
    """

    def __init__(self):
        super(Selected, self).__init__()

        self.selectionerror = QMessageBox(self)
        self.selectionerror.setWindowTitle("Movie Selection Error")
        self.selectionerror.setText("You need to select minimum 5 movies to continue.")
        self.selectionerror.button(QMessageBox.Ok)
        self.selectionerror.setDefaultButton(QMessageBox.Ok)
        self.selectionerror.setStyleSheet("background-color: #FFFAF0; font: 10pt\"MS Shell Dlg 2\";")
        self.selectionerror.setIcon(QMessageBox.Warning)
        self.selectionerror.exec_()


class MyLabel(QLabel):
    def __init__(self, parent=None):
        super(MyLabel, self).__init__(parent)
        self.installEventFilter(self)

    def eventFilter(self, source, event):
        if event.type() == QEvent.MouseButtonPress:
            global _obj_
            _obj_ = source.objectName()
            print(_obj_)

        return super().eventFilter(source, event)


class Checklist(QDialog):
    def __init__(self):
        super(Checklist, self).__init__()
        loadUi("UI\\Checklist UI\\checklist.ui", self)
        self.setWindowTitle("Select Movies - Cinematch")

        self.display_frame_flag = [None, False, False, False, False, False, False]
        self.search_frame_flag = [None, False, False, False, False, False]

        self.exit_button.setIcon(QIcon("Icons\\x-mark-checklist.png"))
        self.exit_button.clicked.connect(self.close_func)

        self.done_button.clicked.connect(self.done_func)

        self.search_field.returnPressed.connect(lambda: self.search_func)
        self.search_button.clicked.connect(self.search_func)

        self.search_error_label = QLabel(self.search_scroll_area_contents)
        self.search_error_label.setStyleSheet('font: 18pt"MS Shell Dlg 2"; color: red;')
        self.search_vlayout.addWidget(self.search_error_label)

        for i in range(1, 7):
            self.new_widgets_display(i)

    def reject(self):
        """
        Pressing esc key results in the screen quitting cuz this built-in function is called, so we are modifying
        it externally to do nothing when the esc key is pressed.
        """
        pass

    def closeEvent(self, event):
        """
        Due to an unknown bug (mostly by modifying reject() function), the close button doesn't work. So we are
        overriding the default closeEvent to close the window when close button is pressed
        """
        self.close()

    def new_widgets_search(self, number):
        # unique identifiers for each frame,image,title in the search tab
        self.s_frame_new = f"s_frame_{number}"
        self.s_image_new = f"s_image_{number}"
        self.s_title_new = f"s_title_{number}"
        print(self.s_frame_new, self.s_image_new, self.s_title_new)

        self.s_frame = QFrame(self.search_scroll_area_contents)
        self.s_frame.setObjectName(self.s_frame_new)
        self.s_frame.setStyleSheet(u"border-radius:1px; background-color:#FFE7FA;")
        self.s_frame.setFrameShape(QFrame.Panel)
        setattr(self, self.s_frame_new, self.s_frame)

        self.frame_hlayout = QHBoxLayout(self.s_frame)
        self.frame_hlayout.setSpacing(30)
        self.frame_hlayout.setObjectName(u"frame_hlayout")

        self.s_movie_image = MyLabel(self.s_frame)
        self.s_movie_image.setObjectName(self.s_image_new)
        self.s_movie_image.setScaledContents(True)
        self.s_movie_image.setFixedSize(QSize(100, 150))
        self.s_movie_image.setCursor(QCursor(Qt.PointingHandCursor))
        self.s_movie_image.setStyleSheet(u"border-radius:10px; background-color:rgb(240, 234, 214);")
        image_object = QImage()
        image_object.loadFromData(image)
        _image = QPixmap(image_object)
        self.s_movie_image.setPixmap(_image)
        setattr(self, self.s_image_new, self.s_movie_image)

        self.s_movie_title = MyLabel(self.s_frame)
        self.s_movie_title.setObjectName(self.s_title_new)
        self.s_movie_title.setCursor(QCursor(Qt.PointingHandCursor))
        self.s_movie_title.setStyleSheet(u"border-radius: 14px; background-color:rgb(255, 231, 250);")
        self.s_movie_title.setText("Ant Man and the Wasp")
        self.s_movie_title.setWordWrap(True)
        self.s_movie_title.hasScaledContents()
        setattr(self, self.s_title_new, self.s_movie_title)

        clickable(self.s_movie_image).connect(self.search_frame_color_change)
        clickable(self.s_movie_title).connect(self.search_frame_color_change)

        self.frame_hlayout.addWidget(self.s_movie_image)
        self.frame_hlayout.addWidget(self.s_movie_title)

        self.search_vlayout.addWidget(self.s_frame, Qt.AlignHCenter | Qt.AlignVCenter)

    def new_widgets_display(self, number):
        # unique identifiers for each frame,image,title in the popular movies
        self.frame_new = f"frame_{number}"
        self.image_new = f"image_{number}"
        self.title_new = f"title_{number}"
        print(self.frame_new, self.image_new, self.title_new)

        self.frame = QFrame(self.popular_scroll_area_contents)
        self.frame.setObjectName(self.frame_new)
        self.frame.setFixedSize(QSize(120, 240))
        self.frame.setStyleSheet(u"border-radius:1px; background-color:#FFE7FA;")
        self.frame.setFrameShape(QFrame.Panel)
        setattr(self, self.frame_new, self.frame)

        self.frame_vlayout = QVBoxLayout(self.frame)
        self.frame_vlayout.setObjectName(u"frame_vlayout")

        self.movie_image = MyLabel(self.frame)
        self.movie_image.setObjectName(self.image_new)
        self.movie_image.setScaledContents(True)
        self.movie_image.setFixedSize(QSize(100, 150))
        self.movie_image.setCursor(QCursor(Qt.PointingHandCursor))
        self.movie_image.setStyleSheet(u"border-radius:10px; background-color:rgb(240, 234, 214);")
        image_object = QImage()
        image_object.loadFromData(image)
        _image = QPixmap(image_object)
        self.movie_image.setPixmap(_image)
        setattr(self, self.image_new, self.movie_image)

        self.movie_title = MyLabel(self.frame)
        self.movie_title.setObjectName(self.title_new)
        self.movie_title.setFixedSize(QSize(100, 60))
        self.movie_title.setCursor(QCursor(Qt.PointingHandCursor))
        self.movie_title.setStyleSheet(u"border-radius:10px; background-color:rgb(255, 231, 250);")
        self.movie_title.setText("Ant Man and the Wasp: Quantumania")
        self.movie_title.setWordWrap(True)
        self.movie_title.hasScaledContents()
        setattr(self, self.title_new, self.movie_title)

        clickable(self.movie_image).connect(self.display_frame_color_change)
        clickable(self.movie_title).connect(self.display_frame_color_change)

        self.frame_vlayout.addWidget(self.movie_image)
        self.frame_vlayout.addWidget(self.movie_title)

        self.popular_hlayout.addWidget(self.frame, Qt.AlignHCenter | Qt.AlignVCenter)

    def search_frame_color_change(self):
        global selected_movies_display, selected_movies_search, real_selected_movies_search

        if _obj_ in ['s_image_1', 's_title_1', 's_frame_1']:
            if not self.search_frame_flag[1]:
                self.s_frame_1.setStyleSheet(frame_css)
                self.s_image_1.setStyleSheet(image_css)
                self.s_title_1.setStyleSheet(title_css)
                self.search_frame_flag[1] = True

            else:
                self.s_frame_1.setStyleSheet(frame_true_css)
                self.search_frame_flag[1] = False

        if _obj_ in ['s_image_2', 's_title_2', 's_frame_2']:
            if not self.search_frame_flag[2]:
                self.s_frame_2.setStyleSheet(frame_css)
                self.s_image_2.setStyleSheet(image_css)
                self.s_title_2.setStyleSheet(title_css)
                self.search_frame_flag[2] = True

            else:
                self.s_frame_2.setStyleSheet(frame_true_css)
                self.search_frame_flag[2] = False

        if _obj_ in ['s_image_3', 's_title_3', 's_frame_3']:
            if not self.search_frame_flag[3]:
                self.s_frame_3.setStyleSheet(frame_css)
                self.s_image_3.setStyleSheet(image_css)
                self.s_title_3.setStyleSheet(title_css)
                self.search_frame_flag[3] = True

            else:
                self.s_frame_3.setStyleSheet(frame_true_css)
                self.search_frame_flag[3] = False

        if _obj_ in ['s_image_4', 's_title_4', 's_frame_4']:
            if not self.search_frame_flag[4]:
                self.s_frame_4.setStyleSheet(frame_css)
                self.s_image_4.setStyleSheet(image_css)
                self.s_title_4.setStyleSheet(title_css)
                self.search_frame_flag[4] = True

            else:
                self.s_frame_4.setStyleSheet(frame_true_css)
                self.search_frame_flag[4] = False

        if _obj_ in ['s_image_5', 's_title_5', 's_frame_5']:
            if not self.search_frame_flag[5]:
                self.s_frame_5.setStyleSheet(frame_css)
                self.s_image_5.setStyleSheet(image_css)
                self.s_title_5.setStyleSheet(title_css)
                self.search_frame_flag[5] = True

            else:
                self.s_frame_5.setStyleSheet(frame_true_css)
                self.search_frame_flag[5] = False

        print(self.search_frame_flag)

        selected_movies_display = self.display_frame_flag.count(True)
        selected_movies_search = self.search_frame_flag.count(True)

        self.selected_text.setText(
            f"Selected movies: {selected_movies_display + selected_movies_search + real_selected_movies_search} (Minimum 5)")

    def display_frame_color_change(self):
        global selected_movies_display, selected_movies_search

        if _obj_ in ['image_1', 'title_1', 'frame_1']:
            if not self.display_frame_flag[1]:
                self.frame_1.setStyleSheet(frame_css)
                self.image_1.setStyleSheet(image_css)
                self.title_1.setStyleSheet(title_css)
                self.display_frame_flag[1] = True

            else:
                self.frame_1.setStyleSheet(frame_true_css)
                self.display_frame_flag[1] = False

        if _obj_ in ['image_2', 'title_2', 'frame_2']:
            if not self.display_frame_flag[2]:
                self.frame_2.setStyleSheet(frame_css)
                self.image_2.setStyleSheet(image_css)
                self.title_2.setStyleSheet(title_css)
                self.display_frame_flag[2] = True

            else:
                self.frame_2.setStyleSheet(frame_true_css)
                self.display_frame_flag[2] = False

        if _obj_ in ['image_3', 'title_3', 'frame_3']:
            if not self.display_frame_flag[3]:
                self.frame_3.setStyleSheet(frame_css)
                self.image_3.setStyleSheet(image_css)
                self.title_3.setStyleSheet(title_css)
                self.display_frame_flag[3] = True

            else:
                self.frame_3.setStyleSheet(frame_true_css)
                self.display_frame_flag[3] = False

        if _obj_ in ['image_4', 'title_4', 'frame_4']:
            if not self.display_frame_flag[4]:
                self.frame_4.setStyleSheet(frame_css)
                self.image_4.setStyleSheet(image_css)
                self.title_4.setStyleSheet(title_css)
                self.display_frame_flag[4] = True

            else:
                self.frame_4.setStyleSheet(frame_true_css)
                self.display_frame_flag[4] = False

        if _obj_ in ['image_5', 'title_5', 'frame_5']:
            if not self.display_frame_flag[5]:
                self.frame_5.setStyleSheet(frame_css)
                self.image_5.setStyleSheet(image_css)
                self.title_5.setStyleSheet(title_css)
                self.display_frame_flag[5] = True

            else:
                self.frame_5.setStyleSheet(frame_true_css)
                self.display_frame_flag[5] = False

        if _obj_ in ['image_6', 'title_6', 'frame_6']:
            if not self.display_frame_flag[6]:
                self.frame_6.setStyleSheet(frame_css)
                self.image_6.setStyleSheet(image_css)
                self.title_6.setStyleSheet(title_css)
                self.display_frame_flag[6] = True

            else:
                self.frame_6.setStyleSheet(frame_true_css)
                self.display_frame_flag[6] = False

        print(self.display_frame_flag)
        print(self.search_frame_flag)


        selected_movies_display = self.display_frame_flag.count(True)
        selected_movies_search = self.search_frame_flag.count(True)

        self.selected_text.setText(
            f"Selected movies: {selected_movies_display + selected_movies_search + real_selected_movies_search} (Minimum 5)")

    def close_func(self):
        self.close()

    def done_func(self):
        if selected_movies_display + selected_movies_search + real_selected_movies_search < 5:
            Selected()
        else:
            # Direct to next (Genres/Languages) page
            print("Moving on to Genres/Languages")

    def search_func(self):
        global real_selected_movies_search, selected_movies_search

        self.search_text = self.search_field.text()
        # execute cursor here

        if self.search_text.strip() == "":  # add one more condition if movie isn't found in the table
            self.search_error_label.setText("No movie found!")

            try:
                self.search_error_label.show()
                self.s_frame_1.hide()
                self.s_frame_2.hide()
                self.s_frame_3.hide()
                self.s_frame_4.hide()
                self.s_frame_5.hide()
                self.s_frame_1.setStyleSheet(frame_true_css)
                self.s_frame_2.setStyleSheet(frame_true_css)
                self.s_frame_3.setStyleSheet(frame_true_css)
                self.s_frame_4.setStyleSheet(frame_true_css)
                self.s_frame_5.setStyleSheet(frame_true_css)

                self.search_frame_flag = [None, False, False, False, False, False]
                real_selected_movies_search += selected_movies_search

            except:
                pass

            print("Movie not found")

        else:
            self.search_error_label.setText("")
            self.search_error_label.hide()
            # search for movie and generate widgets
            try:
                self.s_frame_1.setFrameShape(QFrame.Panel)
            except:
                for i in range(1, 6):
                    self.new_widgets_search(i)
                print("Generating New Frames")
            else:
                self.s_frame_1.show()
                self.s_frame_2.show()
                self.s_frame_3.show()
                self.s_frame_4.show()
                self.s_frame_5.show()
                self.s_frame_1.setStyleSheet(frame_true_css)
                self.s_frame_2.setStyleSheet(frame_true_css)
                self.s_frame_3.setStyleSheet(frame_true_css)
                self.s_frame_4.setStyleSheet(frame_true_css)
                self.s_frame_5.setStyleSheet(frame_true_css)

                self.search_frame_flag = [None, False, False, False, False, False]
                real_selected_movies_search += selected_movies_search
                print("Updating preexisting frames")
                # update preexisting frames here by querying sql


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Checklist()
    window.show()
    sys.exit(app.exec_())
