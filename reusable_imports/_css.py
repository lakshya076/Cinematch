checklist_frame_selection_css = """
border-radius:5px; 
border-color:black black black black; 
background-color: #F0E7FF; 
selection-background-color: black; 
border-width: 2px; 
border-style: solid; 
border-color: rgb(9, 23, 217) rgb(9, 23, 217) rgb(9, 23, 217) rgb(9, 23, 217);
"""

checklist_image_selection_css = """
border-width:0px;
background-color:#F0E7FF;
"""

checklist_title_selection_css = """
border-width:0px;
background-color:#F0E7FF;
font:12pt \"MS Shell Dlg 2\";
"""

genre_frame_selection_css = """
border-radius:5px; 
border-color:black black black black; 
background-color: #F0E7FF; 
selection-background-color: black; 
border-width: 2px; 
border-style: solid; 
border-color: rgb(9, 23, 217) rgb(9, 23, 217) rgb(9, 23, 217) rgb(9, 23, 217);
font:18pt \"MS Shell Dlg 2\";
"""

genre_title_selection_css = """
border-width:0px;
background-color:#F0E7FF;
font:14pt \"MS Shell Dlg 2\";
"""

light_scroll_area_mainwindow = """
    background-color:#FFFAF0;
    color: #000000;
"""
light_movies = """
    QFrame {
        background-color: #FFD173;
    }
    """
light_mainwin_widget = """
    color: #000000;
    background-color:#FFFAF0;
    font:14pt;

    QTextBrowser {
        color:#000000;
        background-color:#FFFAF0;
    }
"""
light_create_css = """
    background-color: #FFFAF0;
    min-height:20px;
    padding:8px;
    font:14pt;
    border: 1px solid #000000;
    border-radius:20px;
    color:black;
    """
light_main_stylesheet = """
        /*CentralWidget Stylesheet*/
        #centralwidget {
            background-color:#FFFAF0;
        }
        
        /*Sidebar css*/
        #collapse {
            background-color: #313A46;
        }
        #collapse QPushButton {
            border:none;
        }
        #expand {
            background-color: #313A46;
        }
        #expand QPushButton {
            border:none;
            text-align: left;
            padding: 8px 0 8px 15px;
            color: #BCD2F5;
            font:12pt \"MS Shell Dlg 2\";
        }
        #expand QPushButton:checked {
            background-color: #FFF;
        }

        /*QScrollBar css*/
        QScrollBar:horizontal {
            border: 1px solid grey;
            height: 8px;
        }
        QScrollBar::handle:horizontal {
            background: #858585;
            min-width: 20px;
        }
        QScrollBar::add-line:horizontal {
            border: 1px solid grey;
            background: black;
            width: 20px;
            subcontrol-position: right;
            subcontrol-origin: margin;
        }
        QScrollBar::sub-line:horizontal {
            border: 1px solid grey;
            background: black;
            width: 20px;
            subcontrol-position: left;
            subcontrol-origin: margin;
        }
        
        /* QLineEdit css */
        QLineEdit {
            padding-left: 10px;
            padding-right: 10px;
            border: 1px solid black;
            border-radius: 20px;
        }
        """

dark_scroll_area_mainwindow = """
    
    background-color: #24292E;
    color: #FFFAF0;

"""
dark_mainwin_widget = """
    color: #FFFAF0;
    background-color:#24292E;
    font: 14pt;

    QTextBrowser {
        color:#FFFAF0;
        background-color:#353a3f;
        font: 14pt;
    }

    """
dark_create_css = """
    background-color: #24292E;
    min-height:20px;
    padding:8px;
    font:14pt;
    border: 1px solid #FFFAF0;
    border-radius:20px;
    color:#FFFAF0;
    """
dark_library_stylesheet = """
    QFrame {
        background-color: #13161a;
        color: #DFE8F5; 
        border-radius: 16px; 
        border-width: 1px;
    }
    QPushButton {
        background-color: rgba(0,0,0,0);
        border:none;
    }
    QToolTip {
        color: #000;
        opacity: 200;
        font: 8pt;
    }
    """
dark_playlist_frame_style = """
    font:14pt;
    background-color: #13161a; 
    color: #fffaf0;
    border-radius: 10px;
    border: 1px solid #13161a;
"""
dark_widget_stylesheet = """
    QFrame {
        background-color: #13161a;
        color: #DFE8F5; 
        border-radius: 16px; 
        border-width: 1px;
    }
"""
dark_main_stylesheet = """
        /*CentralWidget Stylesheet*/
        #centralwidget {
            background-color: #24292E;
            color: #FFFAF0;
        }
        
        /*Sidebar css*/
        #collapse {
            background-color: #313A46;
        }
        #collapse QPushButton {
            border:none;
        }
        #expand {
            background-color: #313A46;
        }
        #expand QPushButton {
            border:none;
            text-align: left;
            padding: 8px 0px 8px 15px;
            color: #BCD2F5;
            font:12pt \"MS Shell Dlg 2\";
        }
        #expand QPushButton:checked {
            color: #ffffff;
        }
        
        /* Taste Profile CSS */
        #widget {
            background-color:#313a46;
            color:#fffaf0;   
        }
        #taste {
            background-color:#313a46;
        }
        
        /*QScrollBar css*/
        QScrollBar:horizontal {
            border: 1px solid grey;
            background: #32CC99;
            height: 10px;
        }        
        QScrollBar::handle:horizontal {
            background: #FFFAF0;
            min-width: 20px;
        }
        QScrollBar::add-line:horizontal {
            border: 2px solid grey;
            background: #32CC99;
            width: 20px;
            subcontrol-position: right;
            subcontrol-origin: margin;
        }
        QScrollBar::sub-line:horizontal {
            border: 2px solid grey;
            background: #32CC99;
            width: 20px;
            subcontrol-position: left;
            subcontrol-origin: margin;
        }
        
        /* QLineEdit css */
        QLineEdit {
            padding-left: 10px;
            padding-right: 10px;
            border-radius: 20px;
            border-width: 1px;
        }
"""
