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

light_scroll_area_mainwindow = "background-color:#FFFAF0; color: #000000;"
light_mainwin_widget = "color: #000000;"
light_tab_widget = "background-color: #FFFAF0;"
light_tab_content = "color: #000000;"
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
            color: #ffffff;
        }
        
        /*QTabWidget css*/
        QTabWidget::pane {
            background-color: #FFFAF0;
        } 
        QTabBar::tab {
            background: #F5F5DC; 
            border: 1px solid black;
            padding: 5px;
            font: 12pt;
            width: 150px;
            height: 30px
        }
        QTabBar::tab:selected { 
            background: #FFFAF0; 
            border-bottom: 0px;
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
            padding: 8px;
        }
        """

dark_scroll_area_mainwindow = "background-color: #24292E; color: #FFFFFF;"
dark_mainwin_widget = "color: #FFFAF0;"
dark_tab_widget = "background-color: #24292E;"
dark_tab_content = "color: #FFFAF0;"
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
        
        /*QTabWidget css*/
        QTabWidget::pane {
            background-color: #24292E;
        }
        QTabBar::tab {
            background: #DFE8F5;
            border: 1px solid #FFFAF0;
            padding: 5px;
            font: 12pt;
            width: 150px;
            height: 30px
        }
        QTabBar::tab:selected { 
            background: #24292E;
            color: #FFFAF0; 
            border-bottom: 0px;
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
            padding: 8px;
        }
"""
