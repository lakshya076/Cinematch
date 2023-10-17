import os
import sys
import requests
from cachecontrol import CacheControl
from cachecontrol.caches import FileCache

from PyQt5.QtCore import QSize, Qt, QEvent
from PyQt5.QtGui import QCursor, QImage, QPixmap, QIcon
from PyQt5.QtWidgets import QFrame, QApplication, QLabel, QVBoxLayout, QDialog
from PyQt5.uic import loadUi

from reusable_imports.commons import ErrorDialog, clickable
from reusable_imports._css import checklist_frame_selection_css, checklist_image_selection_css, \
    checklist_title_selection_css
from reusable_imports.source_vars import checklist_movie_source
from reusable_imports.common_vars import movies

# 168,325 : 150,225 : 150,60 -> preferred layouts of frame, image and title for the main ui page

_obj_ = ""

frame_original = "border-radius:10px; border-width:2px; background-color:#F5F5DC;"
image_original = "border-radius:10px; border-width:2px; background-color:#F5F5DC;"
title_original = "border-radius:10px; background-color:#F5F5DC; font:12pt \"MS Shell Dlg 2\";"


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
    global frame_original, image_original, title_original

    def frame_reuse(self):
        self.frame.setFixedSize(QSize(170, 315))
        self.frame.setStyleSheet(frame_original)
        self.frame.setFrameShape(QFrame.Panel)

    def image_reuse(self):
        self.movie_image.setScaledContents(True)
        self.movie_image.setFixedSize(QSize(150, 225))
        self.movie_image.setCursor(QCursor(Qt.PointingHandCursor))
        self.movie_image.setStyleSheet(image_original)

    def title_reuse(self):
        self.movie_title.setFixedSize(QSize(150, 60))
        self.movie_title.setCursor(QCursor(Qt.PointingHandCursor))
        self.movie_title.setStyleSheet(title_original)
        self.movie_title.setWordWrap(True)
        self.movie_title.hasScaledContents()


class Checklist(QDialog, FrameReuse):
    def __init__(self):
        super(Checklist, self).__init__()
        loadUi("UI\\ui_checklist.ui", self)
        self.setWindowTitle("Select Movies - Cinematch")
        self.stack.setCurrentIndex(0)  # At the start the popular movies are shown first

        global _obj_  # defining global variables for the whole class

        self.frame_flag = [False] * 115
        '''setting up frame flags to know if a frame has been clicked or not so that we could select/deselect the
         frame (apply css)'''

        self.scroll = [self.popular_scroll_area, self.handpicked_scroll_area, self.action_scroll_area,
                       self.animation_scroll_area, self.comedy_scroll_area, self.comedy_scroll_area,
                       self.drama_scroll_area, self.horror_scroll_area, self.romance_scroll_area,
                       self.scifi_scroll_area]
        '''parent objects for the scroll parameter of the new_widgets function'''

        self.exit_button.setIcon(QIcon("Icons/x_checklist.ico"))
        self.exit_button.clicked.connect(self.close_func)
        self.exit_button.setStyleSheet("background-color: rgba(0,0,0,0); font:14pt;")

        self.done_button.clicked.connect(self.done_func)

        # Button click redirects to change the visible page on stacked widget
        self.genre_1.clicked.connect(self.switch_to_1)
        self.genre_2.clicked.connect(self.switch_to_2)
        self.genre_3.clicked.connect(self.switch_to_3)
        self.genre_4.clicked.connect(self.switch_to_4)
        self.genre_5.clicked.connect(self.switch_to_5)
        self.genre_6.clicked.connect(self.switch_to_6)
        self.genre_7.clicked.connect(self.switch_to_7)
        self.genre_8.clicked.connect(self.switch_to_8)
        self.genre_9.clicked.connect(self.switch_to_9)
        self.genre_10.clicked.connect(self.switch_to_10)

        session = CacheControl(requests.Session(), cache=FileCache(
            f"{os.path.expanduser('~')}\\AppData\\Local\\Temp\\CinematchCache\\.chk_img_cache"))
        # Common session used by the frames in the loop to load images from the web. The images are then cached and
        # stored so when the program is run again, images load easily.

        # The following loops below are to generate widgets (frames) with movie images and movie titles with unique
        # names. 10 separate loops are used because the scroll_area of the new_widgets require a different value
        # (scroll_area parent value for the respective QFrame) to associate the widgets of the specific loop to
        # These frames are then displayed on the screen by calling the 10 class method after the loops which put each
        # frame individually in the grid layout of their respective stacked widget
        for i in range(0, 20):
            from_db_1 = checklist_movie_source[i][2]
            url_1 = f"https://image.tmdb.org/t/p/original{from_db_1}"  # Getting the image of the movie
            image_1 = session.get(url_1).content
            self.new_widgets(number=i, img=image_1, title=checklist_movie_source[i][1], scroll_area=self.scroll[0])

        for i in range(20, 30):
            from_db_2 = checklist_movie_source[i][2]
            url_2 = f"https://image.tmdb.org/t/p/original{from_db_2}"
            image_2 = session.get(url_2).content
            self.new_widgets(number=i, img=image_2, title=checklist_movie_source[i][1], scroll_area=self.scroll[1])

        for i in range(30, 40):
            from_db_3 = checklist_movie_source[i][2]
            url_3 = f"https://image.tmdb.org/t/p/original{from_db_3}"
            image_3 = session.get(url_3).content
            self.new_widgets(number=i, img=image_3, title=checklist_movie_source[i][1], scroll_area=self.scroll[2])

        for i in range(40, 50):
            from_db_4 = checklist_movie_source[i][2]
            url_4 = f"https://image.tmdb.org/t/p/original{from_db_4}"
            image_4 = session.get(url_4).content
            self.new_widgets(number=i, img=image_4, title=checklist_movie_source[i][1], scroll_area=self.scroll[3])

        for i in range(50, 60):
            from_db_5 = checklist_movie_source[i][2]
            url_5 = f"https://image.tmdb.org/t/p/original{from_db_5}"
            image_5 = session.get(url_5).content
            self.new_widgets(number=i, img=image_5, title=checklist_movie_source[i][1], scroll_area=self.scroll[4])

        for i in range(60, 70):
            from_db_6 = checklist_movie_source[i][2]
            url_6 = f"https://image.tmdb.org/t/p/original{from_db_6}"
            image_6 = session.get(url_6).content
            self.new_widgets(number=i, img=image_6, title=checklist_movie_source[i][1], scroll_area=self.scroll[5])

        for i in range(70, 80):
            from_db_7 = checklist_movie_source[i][2]
            url_7 = f"https://image.tmdb.org/t/p/original{from_db_7}"
            image_7 = session.get(url_7).content
            self.new_widgets(number=i, img=image_7, title=checklist_movie_source[i][1], scroll_area=self.scroll[6])

        for i in range(80, 90):
            from_db_8 = checklist_movie_source[i][2]
            url_8 = f"https://image.tmdb.org/t/p/original{from_db_8}"
            image_8 = session.get(url_8).content
            self.new_widgets(number=i, img=image_8, title=checklist_movie_source[i][1], scroll_area=self.scroll[7])

        for i in range(90, 100):
            from_db_9 = checklist_movie_source[i][2]
            url_9 = f"https://image.tmdb.org/t/p/original{from_db_9}"
            image_2 = session.get(url_9).content
            self.new_widgets(number=i, img=image_2, title=checklist_movie_source[i][1], scroll_area=self.scroll[8])

        for i in range(100, 115):
            from_db_10 = checklist_movie_source[i][2]
            url_10 = f"https://image.tmdb.org/t/p/original{from_db_10}"
            image_10 = session.get(url_10).content
            self.new_widgets(number=i, img=image_10, title=checklist_movie_source[i][1], scroll_area=self.scroll[9])

        self.add_to_1()  # Function to add some widgets to the popular page's grid layout for the user to view
        self.add_to_2()  # Function to add some widgets to the popular page's grid layout for the user to view
        self.add_to_3()  # Function to add some widgets to the popular page's grid layout for the user to view
        self.add_to_4()  # Function to add some widgets to the popular page's grid layout for the user to view
        self.add_to_5()  # Function to add some widgets to the popular page's grid layout for the user to view
        self.add_to_6()  # Function to add some widgets to the popular page's grid layout for the user to view
        self.add_to_7()  # Function to add some widgets to the popular page's grid layout for the user to view
        self.add_to_8()  # Function to add some widgets to the popular page's grid layout for the user to view
        self.add_to_9()  # Function to add some widgets to the popular page's grid layout for the user to view
        self.add_to_10()  # Function to add some widgets to the popular page's grid layout for the user to view

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
        If it greater than or equal to 5, accept flag is returned and we move on to Genres/Languages page.
        :return: None
        """

        if len(movies) < 5:
            selected_error = ErrorDialog()
            selected_error.error_dialog.setWindowTitle("Movie Selection Error!")
            selected_error.error_dialog.setText("You need to select minimum 5 movies to continue.")
            selected_error.error_dialog.exec_()
        else:
            # Direct to next (Genres/Languages) page
            print("Moving on to Genres/Languages")
            self.accept()

    def new_widgets(self, number, img, title, scroll_area):
        # unique identifiers for each frame,image,title
        self.frame_new = f"frame_{number}"
        self.image_new = f"image_{number}"
        self.title_new = f"title_{number}"
        print(self.frame_new, self.image_new, self.title_new)

        # generic frame object
        self.frame = QFrame(scroll_area)  # the scroll area parent which QFrame will belong to
        self.frame.setObjectName(self.frame_new)
        self.frame_reuse()  # calls the frame reuse method from frame reuse class so to setup frame properties.
        setattr(self, self.frame_new, self.frame)

        # creating a vlayout to store the contents which will be put inside the frame (movie image and movie title)
        self.frame_vlayout = QVBoxLayout(self.frame)
        self.frame_vlayout.setObjectName(u"frame_vlayout")

        # generic movie image object
        self.movie_image = MyLabel(self.frame)
        self.movie_image.setObjectName(self.image_new)
        self.image_reuse()  # calls the image reuse method from frame reuse class so to setup movie image properties.
        image_object = QImage()  # initialising a QImage object
        image_object.loadFromData(img)  # parameter of function (reference to the for loop in __init__ method)
        _image = QPixmap(image_object)  # converting QImage object to QPixmap object to display on the label
        self.movie_image.setPixmap(_image)  # setting the QPixmap object on the image label to display the image
        setattr(self, self.image_new, self.movie_image)

        # generic movie title object
        self.movie_title = MyLabel(self.frame)  # MyLabel is the redefined QLabel class above
        self.movie_title.setObjectName(self.title_new)
        self.title_reuse()  # calls the title reuse method from frame reuse class so to setup movie title properties.
        self.movie_title.setText(title)  # parameter of function (reference to the for loop in __init__ method)
        setattr(self, self.title_new, self.movie_title)

        # Making movie_image and movie_title object clickable externally since Labels don't have an inbuilt click method
        clickable(self.movie_image).connect(self.display_frame_color_change)
        clickable(self.movie_title).connect(self.display_frame_color_change)

        # Adding movie image and movie title objects to the vlayout of the frame
        self.frame_vlayout.addWidget(self.movie_image)
        self.frame_vlayout.addWidget(self.movie_title)

    def display_frame_color_change(self):
        """
        This method is called when a movie_image and movie_title with a specific name is clicked in the ui.
        This method call the frame_selection_reuse function which will decide when the frame is selected or deselected
        and when a movie should be added in the movies list and when it should be removed.
        :return: None
        """

        # _obj_ stores the id of the clicked object and this variable extracts the number of the object clicked
        obj = _obj_.split(sep='_')[1]

        self.frame_selection_reuse(frame=f"frame_{obj}", title=f"title_{obj}", image=f"image_{obj}", number=int(obj))

        # Displays the selected movies in the ui (bottom right)
        self.selected_text.setText(f"Selected movies: {self.frame_flag.count(True)} (Minimum 5)")

    def frame_selection_reuse(self, frame, title, image, number):
        """
        The main use of this function is to change the status of a movie_frame when a mouse press is detected.
        If the frame_flag for the specific movie is False, the movie is 'selected' and thus highlighted and its id is
        added to the movies list which will passed in the algorithm.
        If the frame_flag for the specific movie is True, the movie is 'deselected' and thus highlight is removed and
        its id is removed from the movies list.
        The frame_flag above is a member of the self.frame_flag list (depending on the clicked frame) defined in
        the __init__ method.
        This function will be called in the frame_color_change method which is called when a movie_image and movie_title
        with a specific, unique id is clicked in the ui.
        :param frame: str -> frame_number (will be passed as eval)
        :param title: str -> title_number (will be passed as eval)
        :param image: str -> image_number (will be passed as eval)
        :param number: int -> the number in frame_number, title_number, image_number
        :return: None
        """

        if _obj_ in [frame, title, image]:
            if not self.frame_flag[number]:
                eval(f"self.{frame}.setStyleSheet(checklist_frame_selection_css)")
                eval(f"self.{image}.setStyleSheet(checklist_image_selection_css)")
                eval(f"self.{title}.setStyleSheet(checklist_title_selection_css)")
                self.frame_flag[number] = True

                try:
                    movies.append(checklist_movie_source[number][0])
                except:
                    pass

            else:
                eval(f"self.{frame}.setStyleSheet(frame_original)")
                eval(f"self.{image}.setStyleSheet(image_original)")
                eval(f"self.{title}.setStyleSheet(title_original)")
                self.frame_flag[number] = False

                try:
                    movies.remove(checklist_movie_source[number][0])
                except:
                    pass

            print(movies)

    # Functions to add to scroll areas of different pages in stacked widget
    def add_to_1(self):
        """
        This function adds frames 1 to 20 (auto generated above) to the popular_grid grid layout which helps the
        frames get displayed
        :return: None
        """

        self.popular_grid.addWidget(self.frame_0, 1, 1, Qt.AlignHCenter | Qt.AlignVCenter)
        self.popular_grid.addWidget(self.frame_1, 1, 2, Qt.AlignHCenter | Qt.AlignVCenter)
        self.popular_grid.addWidget(self.frame_2, 1, 3, Qt.AlignHCenter | Qt.AlignVCenter)
        self.popular_grid.addWidget(self.frame_3, 1, 4, Qt.AlignHCenter | Qt.AlignVCenter)
        self.popular_grid.addWidget(self.frame_4, 1, 5, Qt.AlignHCenter | Qt.AlignVCenter)
        self.popular_grid.addWidget(self.frame_5, 2, 1, Qt.AlignHCenter | Qt.AlignVCenter)
        self.popular_grid.addWidget(self.frame_6, 2, 2, Qt.AlignHCenter | Qt.AlignVCenter)
        self.popular_grid.addWidget(self.frame_7, 2, 3, Qt.AlignHCenter | Qt.AlignVCenter)
        self.popular_grid.addWidget(self.frame_8, 2, 4, Qt.AlignHCenter | Qt.AlignVCenter)
        self.popular_grid.addWidget(self.frame_9, 2, 5, Qt.AlignHCenter | Qt.AlignVCenter)
        self.popular_grid.addWidget(self.frame_10, 3, 1, Qt.AlignHCenter | Qt.AlignVCenter)
        self.popular_grid.addWidget(self.frame_11, 3, 2, Qt.AlignHCenter | Qt.AlignVCenter)
        self.popular_grid.addWidget(self.frame_12, 3, 3, Qt.AlignHCenter | Qt.AlignVCenter)
        self.popular_grid.addWidget(self.frame_13, 3, 4, Qt.AlignHCenter | Qt.AlignVCenter)
        self.popular_grid.addWidget(self.frame_14, 3, 5, Qt.AlignHCenter | Qt.AlignVCenter)
        self.popular_grid.addWidget(self.frame_15, 4, 1, Qt.AlignHCenter | Qt.AlignVCenter)
        self.popular_grid.addWidget(self.frame_16, 4, 2, Qt.AlignHCenter | Qt.AlignVCenter)
        self.popular_grid.addWidget(self.frame_17, 4, 3, Qt.AlignHCenter | Qt.AlignVCenter)
        self.popular_grid.addWidget(self.frame_18, 4, 4, Qt.AlignHCenter | Qt.AlignVCenter)
        self.popular_grid.addWidget(self.frame_19, 4, 5, Qt.AlignHCenter | Qt.AlignVCenter)

    def add_to_2(self):
        self.handpicked_grid.addWidget(self.frame_20, 1, 1, Qt.AlignHCenter | Qt.AlignVCenter)
        self.handpicked_grid.addWidget(self.frame_21, 1, 2, Qt.AlignHCenter | Qt.AlignVCenter)
        self.handpicked_grid.addWidget(self.frame_22, 1, 3, Qt.AlignHCenter | Qt.AlignVCenter)
        self.handpicked_grid.addWidget(self.frame_23, 1, 4, Qt.AlignHCenter | Qt.AlignVCenter)
        self.handpicked_grid.addWidget(self.frame_24, 1, 5, Qt.AlignHCenter | Qt.AlignVCenter)
        self.handpicked_grid.addWidget(self.frame_25, 2, 1, Qt.AlignHCenter | Qt.AlignVCenter)
        self.handpicked_grid.addWidget(self.frame_26, 2, 2, Qt.AlignHCenter | Qt.AlignVCenter)
        self.handpicked_grid.addWidget(self.frame_27, 2, 3, Qt.AlignHCenter | Qt.AlignVCenter)
        self.handpicked_grid.addWidget(self.frame_28, 2, 4, Qt.AlignHCenter | Qt.AlignVCenter)
        self.handpicked_grid.addWidget(self.frame_29, 2, 5, Qt.AlignHCenter | Qt.AlignVCenter)

    def add_to_3(self):
        self.action_grid.addWidget(self.frame_30, 1, 1, Qt.AlignHCenter | Qt.AlignVCenter)
        self.action_grid.addWidget(self.frame_31, 1, 2, Qt.AlignHCenter | Qt.AlignVCenter)
        self.action_grid.addWidget(self.frame_32, 1, 3, Qt.AlignHCenter | Qt.AlignVCenter)
        self.action_grid.addWidget(self.frame_33, 1, 4, Qt.AlignHCenter | Qt.AlignVCenter)
        self.action_grid.addWidget(self.frame_34, 1, 5, Qt.AlignHCenter | Qt.AlignVCenter)
        self.action_grid.addWidget(self.frame_35, 2, 1, Qt.AlignHCenter | Qt.AlignVCenter)
        self.action_grid.addWidget(self.frame_36, 2, 2, Qt.AlignHCenter | Qt.AlignVCenter)
        self.action_grid.addWidget(self.frame_37, 2, 3, Qt.AlignHCenter | Qt.AlignVCenter)
        self.action_grid.addWidget(self.frame_38, 2, 4, Qt.AlignHCenter | Qt.AlignVCenter)
        self.action_grid.addWidget(self.frame_39, 2, 5, Qt.AlignHCenter | Qt.AlignVCenter)

    def add_to_4(self):
        self.animation_grid.addWidget(self.frame_40, 1, 1, Qt.AlignHCenter | Qt.AlignVCenter)
        self.animation_grid.addWidget(self.frame_41, 1, 2, Qt.AlignHCenter | Qt.AlignVCenter)
        self.animation_grid.addWidget(self.frame_42, 1, 3, Qt.AlignHCenter | Qt.AlignVCenter)
        self.animation_grid.addWidget(self.frame_43, 1, 4, Qt.AlignHCenter | Qt.AlignVCenter)
        self.animation_grid.addWidget(self.frame_44, 1, 5, Qt.AlignHCenter | Qt.AlignVCenter)
        self.animation_grid.addWidget(self.frame_45, 2, 1, Qt.AlignHCenter | Qt.AlignVCenter)
        self.animation_grid.addWidget(self.frame_46, 2, 2, Qt.AlignHCenter | Qt.AlignVCenter)
        self.animation_grid.addWidget(self.frame_47, 2, 3, Qt.AlignHCenter | Qt.AlignVCenter)
        self.animation_grid.addWidget(self.frame_48, 2, 4, Qt.AlignHCenter | Qt.AlignVCenter)
        self.animation_grid.addWidget(self.frame_49, 2, 5, Qt.AlignHCenter | Qt.AlignVCenter)

    def add_to_5(self):
        self.comedy_grid.addWidget(self.frame_50, 1, 1, Qt.AlignHCenter | Qt.AlignVCenter)
        self.comedy_grid.addWidget(self.frame_51, 1, 2, Qt.AlignHCenter | Qt.AlignVCenter)
        self.comedy_grid.addWidget(self.frame_52, 1, 3, Qt.AlignHCenter | Qt.AlignVCenter)
        self.comedy_grid.addWidget(self.frame_53, 1, 4, Qt.AlignHCenter | Qt.AlignVCenter)
        self.comedy_grid.addWidget(self.frame_54, 1, 5, Qt.AlignHCenter | Qt.AlignVCenter)
        self.comedy_grid.addWidget(self.frame_55, 2, 1, Qt.AlignHCenter | Qt.AlignVCenter)
        self.comedy_grid.addWidget(self.frame_56, 2, 2, Qt.AlignHCenter | Qt.AlignVCenter)
        self.comedy_grid.addWidget(self.frame_57, 2, 3, Qt.AlignHCenter | Qt.AlignVCenter)
        self.comedy_grid.addWidget(self.frame_58, 2, 4, Qt.AlignHCenter | Qt.AlignVCenter)
        self.comedy_grid.addWidget(self.frame_59, 2, 5, Qt.AlignHCenter | Qt.AlignVCenter)

    def add_to_6(self):
        self.crime_grid.addWidget(self.frame_60, 1, 1, Qt.AlignHCenter | Qt.AlignVCenter)
        self.crime_grid.addWidget(self.frame_61, 1, 2, Qt.AlignHCenter | Qt.AlignVCenter)
        self.crime_grid.addWidget(self.frame_62, 1, 3, Qt.AlignHCenter | Qt.AlignVCenter)
        self.crime_grid.addWidget(self.frame_63, 1, 4, Qt.AlignHCenter | Qt.AlignVCenter)
        self.crime_grid.addWidget(self.frame_64, 1, 5, Qt.AlignHCenter | Qt.AlignVCenter)
        self.crime_grid.addWidget(self.frame_65, 2, 1, Qt.AlignHCenter | Qt.AlignVCenter)
        self.crime_grid.addWidget(self.frame_66, 2, 2, Qt.AlignHCenter | Qt.AlignVCenter)
        self.crime_grid.addWidget(self.frame_67, 2, 3, Qt.AlignHCenter | Qt.AlignVCenter)
        self.crime_grid.addWidget(self.frame_68, 2, 4, Qt.AlignHCenter | Qt.AlignVCenter)
        self.crime_grid.addWidget(self.frame_69, 2, 5, Qt.AlignHCenter | Qt.AlignVCenter)

    def add_to_7(self):
        self.drama_grid.addWidget(self.frame_70, 1, 1, Qt.AlignHCenter | Qt.AlignVCenter)
        self.drama_grid.addWidget(self.frame_71, 1, 2, Qt.AlignHCenter | Qt.AlignVCenter)
        self.drama_grid.addWidget(self.frame_72, 1, 3, Qt.AlignHCenter | Qt.AlignVCenter)
        self.drama_grid.addWidget(self.frame_73, 1, 4, Qt.AlignHCenter | Qt.AlignVCenter)
        self.drama_grid.addWidget(self.frame_74, 1, 5, Qt.AlignHCenter | Qt.AlignVCenter)
        self.drama_grid.addWidget(self.frame_75, 2, 1, Qt.AlignHCenter | Qt.AlignVCenter)
        self.drama_grid.addWidget(self.frame_76, 2, 2, Qt.AlignHCenter | Qt.AlignVCenter)
        self.drama_grid.addWidget(self.frame_77, 2, 3, Qt.AlignHCenter | Qt.AlignVCenter)
        self.drama_grid.addWidget(self.frame_78, 2, 4, Qt.AlignHCenter | Qt.AlignVCenter)
        self.drama_grid.addWidget(self.frame_79, 2, 5, Qt.AlignHCenter | Qt.AlignVCenter)

    def add_to_8(self):
        self.horror_grid.addWidget(self.frame_80, 1, 1, Qt.AlignHCenter | Qt.AlignVCenter)
        self.horror_grid.addWidget(self.frame_81, 1, 2, Qt.AlignHCenter | Qt.AlignVCenter)
        self.horror_grid.addWidget(self.frame_82, 1, 3, Qt.AlignHCenter | Qt.AlignVCenter)
        self.horror_grid.addWidget(self.frame_83, 1, 4, Qt.AlignHCenter | Qt.AlignVCenter)
        self.horror_grid.addWidget(self.frame_84, 1, 5, Qt.AlignHCenter | Qt.AlignVCenter)
        self.horror_grid.addWidget(self.frame_85, 2, 1, Qt.AlignHCenter | Qt.AlignVCenter)
        self.horror_grid.addWidget(self.frame_86, 2, 2, Qt.AlignHCenter | Qt.AlignVCenter)
        self.horror_grid.addWidget(self.frame_87, 2, 3, Qt.AlignHCenter | Qt.AlignVCenter)
        self.horror_grid.addWidget(self.frame_88, 2, 4, Qt.AlignHCenter | Qt.AlignVCenter)
        self.horror_grid.addWidget(self.frame_89, 2, 5, Qt.AlignHCenter | Qt.AlignVCenter)

    def add_to_9(self):
        self.romance_grid.addWidget(self.frame_90, 1, 1, Qt.AlignHCenter | Qt.AlignVCenter)
        self.romance_grid.addWidget(self.frame_91, 1, 2, Qt.AlignHCenter | Qt.AlignVCenter)
        self.romance_grid.addWidget(self.frame_92, 1, 3, Qt.AlignHCenter | Qt.AlignVCenter)
        self.romance_grid.addWidget(self.frame_93, 1, 4, Qt.AlignHCenter | Qt.AlignVCenter)
        self.romance_grid.addWidget(self.frame_94, 1, 5, Qt.AlignHCenter | Qt.AlignVCenter)
        self.romance_grid.addWidget(self.frame_95, 2, 1, Qt.AlignHCenter | Qt.AlignVCenter)
        self.romance_grid.addWidget(self.frame_96, 2, 2, Qt.AlignHCenter | Qt.AlignVCenter)
        self.romance_grid.addWidget(self.frame_97, 2, 3, Qt.AlignHCenter | Qt.AlignVCenter)
        self.romance_grid.addWidget(self.frame_98, 2, 4, Qt.AlignHCenter | Qt.AlignVCenter)
        self.romance_grid.addWidget(self.frame_99, 2, 5, Qt.AlignHCenter | Qt.AlignVCenter)

    def add_to_10(self):
        self.scifi_grid.addWidget(self.frame_100, 1, 1, Qt.AlignHCenter | Qt.AlignVCenter)
        self.scifi_grid.addWidget(self.frame_101, 1, 2, Qt.AlignHCenter | Qt.AlignVCenter)
        self.scifi_grid.addWidget(self.frame_102, 1, 3, Qt.AlignHCenter | Qt.AlignVCenter)
        self.scifi_grid.addWidget(self.frame_103, 1, 4, Qt.AlignHCenter | Qt.AlignVCenter)
        self.scifi_grid.addWidget(self.frame_104, 1, 5, Qt.AlignHCenter | Qt.AlignVCenter)
        self.scifi_grid.addWidget(self.frame_105, 2, 1, Qt.AlignHCenter | Qt.AlignVCenter)
        self.scifi_grid.addWidget(self.frame_106, 2, 2, Qt.AlignHCenter | Qt.AlignVCenter)
        self.scifi_grid.addWidget(self.frame_107, 2, 3, Qt.AlignHCenter | Qt.AlignVCenter)
        self.scifi_grid.addWidget(self.frame_108, 2, 4, Qt.AlignHCenter | Qt.AlignVCenter)
        self.scifi_grid.addWidget(self.frame_109, 2, 5, Qt.AlignHCenter | Qt.AlignVCenter)
        self.scifi_grid.addWidget(self.frame_110, 3, 1, Qt.AlignHCenter | Qt.AlignVCenter)
        self.scifi_grid.addWidget(self.frame_111, 3, 2, Qt.AlignHCenter | Qt.AlignVCenter)
        self.scifi_grid.addWidget(self.frame_112, 3, 3, Qt.AlignHCenter | Qt.AlignVCenter)
        self.scifi_grid.addWidget(self.frame_113, 3, 4, Qt.AlignHCenter | Qt.AlignVCenter)
        self.scifi_grid.addWidget(self.frame_114, 3, 5, Qt.AlignHCenter | Qt.AlignVCenter)

    # Stacked Widget switch page functions
    def switch_to_1(self):
        self.stack.setCurrentIndex(0)
        self.genre_define.setText("Popular Movies")

    def switch_to_2(self):
        self.stack.setCurrentIndex(1)
        self.genre_define.setText("Handpicked Movies")

    def switch_to_3(self):
        self.stack.setCurrentIndex(2)
        self.genre_define.setText("Action Movies")

    def switch_to_4(self):
        self.stack.setCurrentIndex(3)
        self.genre_define.setText("Animation Movies")

    def switch_to_5(self):
        self.stack.setCurrentIndex(4)
        self.genre_define.setText("Comedy Movies")

    def switch_to_6(self):
        self.stack.setCurrentIndex(5)
        self.genre_define.setText("Crime Movies")

    def switch_to_7(self):
        self.stack.setCurrentIndex(6)
        self.genre_define.setText("Drama Movies")

    def switch_to_8(self):
        self.stack.setCurrentIndex(7)
        self.genre_define.setText("Horro Movies")

    def switch_to_9(self):
        self.stack.setCurrentIndex(8)
        self.genre_define.setText("Romance Movies")

    def switch_to_10(self):
        self.stack.setCurrentIndex(9)
        self.genre_define.setText("Sci-Fi Movies")

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
        sys.exit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Checklist()
    window.show()
    sys.exit(app.exec_())
