"""
Science Fiction Image by
https://www.freepik.com/free-ai-image/digital-city-life-shines-futuristic-sunset-generated-by-ai_41438711.htm#query=science%20fiction&position=0&from_view=search&track=ais
Adventure Image by
https://www.freepik.com/free-ai-image/one-person-standing-backpack-cliff-edge-generated-by-ai_41594365.htm#fromView=search&term=adventure+movie&page=1&position=2&track=ais_ai_generated
horror - /wVYREutTvI2tmxr6ujrHT704wGF.jpg
comedy - /iuFNMS8U5cb6xfzi51Dbkovj7vM.jpg
"""

import sys

from PyQt5.QtCore import QSize, Qt, QEvent
from PyQt5.QtGui import QCursor, QImage, QPixmap, QIcon
from PyQt5.QtWidgets import QFrame, QApplication, QLabel, QVBoxLayout, QDialog, QHBoxLayout
from PyQt5.uic import loadUi

from reusable_imports.commons import ErrorDialog, clickable
from reusable_imports._css import genre_frame_selection_css, genre_title_selection_css
from reusable_imports.source_vars import genre_source
from reusable_imports.common_vars import genres, languages

# 168,325 : 150,225 : 150,60 -> preferred layouts of frame, image and title for the main ui page

_obj_ = ""

frame_original = "border-radius:10px; border-width:2px; background-color:#F5F5DC;"
title_original = "border-radius:10px; background-color:#F5F5DC; font:18pt \"MS Shell Dlg 2\";"


class MyLabel(QLabel):
    def __init__(self, parent=None):
        super(MyLabel, self).__init__(parent)
        self.installEventFilter(self)

    def eventFilter(self, source, event):
        if event.type() == QEvent.MouseButtonPress:
            global _obj_
            _obj_ = source.objectName()
            print(f"Clicked {_obj_}")

        return super().eventFilter(source, event)


class FrameReuse:
    global frame_original, title_original

    def frame_reuse(self):
        self.frame.setStyleSheet(frame_original)
        self.frame.setFrameShape(QFrame.Panel)

    def title_reuse(self):
        self.movie_title.setCursor(QCursor(Qt.PointingHandCursor))
        self.movie_title.setStyleSheet(title_original)
        self.movie_title.setWordWrap(True)
        self.movie_title.hasScaledContents()


class GenreLang(QDialog, FrameReuse):
    def __init__(self):
        super(GenreLang, self).__init__()
        loadUi("UI\\ui_genre_lang.ui", self)
        self.setWindowTitle("Select Genres/Languages - Cinematch")

        global _obj_  # defining global variables for the whole class

        self.genre_flags = [False] * 15
        '''setting up genre flags to know if a frame has been clicked or not so that we could select/deselect the
         frame (apply css)'''

        self.scroll = [self.genre_scroll, self.lang_scroll]
        '''parent objects for the scroll parameter of the new_widgets function'''

        self.exit_button.setIcon(QIcon("Icons\\x-mark-checklist.png"))
        self.exit_button.clicked.connect(self.close_func)

        self.done_button.clicked.connect(self.done_func)

        """The following loops below are to generate widgets (frames) with movie titles with unique
         names. 2 separate loops are used because the scroll_area of the new_widgets require a different value
         (scroll_area parent value for the respective QFrame) to associate the widgets of the specific loop to
         These frames are then displayed on the screen by calling the 10 class method after the loops which put each
         frame individually in the grid layout of their respective stacked widget
         """
        for i in range(len(genre_source)):
            self.new_widgets(number=i, title=genre_source[i], scroll_area=self.scroll[0])
            eval(f"self.genre_scroll_vlayout.addWidget(self.frame_{i})")

    def new_widgets(self, number, title, scroll_area):
        # unique identifiers for each frame,image,title
        self.frame_new = f"frame_{number}"
        self.title_new = f"title_{number}"
        print(self.frame_new, self.title_new)

        # generic frame object
        self.frame = QFrame(scroll_area)  # the scroll area parent which QFrame will belong to
        self.frame.setObjectName(self.frame_new)
        self.frame_reuse()  # calls the frame reuse method from frame reuse class so to setup frame properties.
        setattr(self, self.frame_new, self.frame)

        # creating a hlayout to store the contents which will be put inside the frame (movie image and movie title)
        self.frame_hlayout = QHBoxLayout(self.frame)
        self.frame_hlayout.setObjectName(u"frame_hlayout")

        # generic movie title object
        self.movie_title = MyLabel(self.frame)  # MyLabel is the redefined QLabel class above
        self.movie_title.setObjectName(self.title_new)
        self.title_reuse()  # calls the title reuse method from frame reuse class so to setup movie title properties.
        self.movie_title.setText(title)  # parameter of function (reference to the for loop in __init__ method)
        setattr(self, self.title_new, self.movie_title)

        # Making movie_image and movie_title object clickable externally since Labels don't have an inbuilt click method
        clickable(self.movie_title).connect(self.display_frame_color_change)

        # Adding movie image and movie title objects to the vlayout of the frame
        self.frame_hlayout.addWidget(self.movie_title)

    def display_frame_color_change(self):
        """
        This method is called when a movie_image and movie_title with a specific name is clicked in the ui.
        This method call the frame_selection_reuse function which will decide when the frame is selected or deselected
        and when a movie should be added in the movies list and when it should be removed.
        :return: None
        """

        # _obj_ stores the id of the clicked object and this variable extracts the number of the object clicked
        obj = _obj_.split(sep='_')[1]

        self.frame_selection_reuse(frame=f"frame_{obj}", title=f"title_{obj}", number=int(obj))

        # Displays the selected movies in the ui (bottom right)
        self.selected_genre_text.setText(f"Selected genres: {self.genre_flags.count(True)} (Minimum 5)")

    def frame_selection_reuse(self, frame, title, number):
        """
        The main use of this function is to change the status of a movie_frame when a mouse press is detected.
        If the frame_flag for the specific movie is False, the movie is 'selected' and thus highlighted and its id is
        added to the movies list which will passed in the algorithm.
        If the frame_flag for the specific movie is True, the movie is 'deselected' and thus highlight is removed and
        its id is removed from the movies list.
        The frame_flag above is a member of the self.genre_flags list (depending on the clicked frame) defined in
        the __init__ method.
        This function will be called in the frame_color_change method which is called when a movie_image and movie_title
        with a specific, unique id is clicked in the ui.
        :param frame: str -> frame_number (will be passed as eval)
        :param title: str -> title_number (will be passed as eval)
        :param number: int -> the number in frame_number, title_number, image_number
        :return: None
        """

        if _obj_ in [frame, title]:
            if not self.genre_flags[number]:
                eval(f"self.{frame}.setStyleSheet(genre_frame_selection_css)")
                eval(f"self.{title}.setStyleSheet(genre_title_selection_css)")
                self.genre_flags[number] = True

                try:
                    genres.append(genre_source[number])
                except:
                    pass

            else:
                eval(f"self.{frame}.setStyleSheet(frame_original)")
                eval(f"self.{title}.setStyleSheet(title_original)")
                self.genre_flags[number] = False

                try:
                    genres.remove(genre_source[number])
                except:
                    pass

            print(genres)

    def close_func(self):
        """
        Exits the program
        :return: None
        """
        self.close()

    def done_func(self):
        """
        Checks if the number of movie_id in movies list is less than 5 or not.
        If it is less than 5, a dialog box is displayed saying minimum 5 movies are required.
        If it greater than or equal to 5, accept flag is returned, and we move on to Genres/Languages page.
        :return: None
        """

        if len(genres) < 1:
            selected_error = ErrorDialog()
            selected_error.error_dialog.setWindowTitle("Genre Selected Error!")
            selected_error.error_dialog.setText("You need to select at least 1 genre to continue.")
            selected_error.error_dialog.exec_()
        else:
            # Direct to next (Genres/Languages) page
            print("Moving on to Splash Screen")
            self.accept()

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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GenreLang()
    window.show()
    sys.exit(app.exec_())
