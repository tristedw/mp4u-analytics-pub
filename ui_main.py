# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainkhojVu.ui'
##
## Created by: Qt User Interface Compiler version 6.4.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLabel,
    QMainWindow, QSizePolicy, QSpacerItem, QStackedWidget,
    QVBoxLayout, QWidget)

class Ui_main_window(object):
    def setupUi(self, main_window):
        if not main_window.objectName():
            main_window.setObjectName(u"main_window")
        main_window.resize(1229, 738)
        main_window.setMinimumSize(QSize(960, 540))
        self.central_widget = QWidget(main_window)
        self.central_widget.setObjectName(u"central_widget")
        self.central_widget.setStyleSheet(u"/* Central Widget */\n"
"#central_widget {\n"
"	background-color: #282a36;\n"
"}\n"
"/* Left Menu */\n"
"#left_menu {\n"
"	background-color: #44475a;\n"
"}\n"
"#left_menu #user_picture {\n"
"	background-color: #282a36;\n"
"	border-radius: 25px;\n"
"	border: 3px solid #565a71;\n"
"}\n"
"/* Content */\n"
"#content {\n"
"	background-color: #282a36;\n"
"}\n"
"/* Pages */\n"
"#pages_container {\n"
"	background-color: #282a36;\n"
"}\n"
"#pages_container .QLabel {\n"
"	font: 18pt \"Segoe UI\";\n"
"	color: rgb(255, 255, 255);\n"
"}\n"
"\n"
"/* Bottom */\n"
"#bottom_credits { \n"
"	background-color: #21232d;\n"
"}\n"
"#bottom_credits .QLabel { \n"
"	color: #6272a4;\n"
"}\n"
"")
        self.verticalLayout_4 = QVBoxLayout(self.central_widget)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.app_frame = QFrame(self.central_widget)
        self.app_frame.setObjectName(u"app_frame")
        self.app_frame.setFrameShape(QFrame.NoFrame)
        self.app_frame.setFrameShadow(QFrame.Raised)
        self.app_layout = QHBoxLayout(self.app_frame)
        self.app_layout.setSpacing(0)
        self.app_layout.setObjectName(u"app_layout")
        self.app_layout.setContentsMargins(0, 0, 0, 0)
        self.left_menu = QFrame(self.app_frame)
        self.left_menu.setObjectName(u"left_menu")
        self.left_menu.setMinimumSize(QSize(60, 0))
        self.left_menu.setMaximumSize(QSize(60, 16777215))
        self.left_menu.setFrameShape(QFrame.NoFrame)
        self.left_menu.setFrameShadow(QFrame.Raised)
        self.left_menu_layout = QVBoxLayout(self.left_menu)
        self.left_menu_layout.setSpacing(0)
        self.left_menu_layout.setObjectName(u"left_menu_layout")
        self.left_menu_layout.setContentsMargins(0, 0, 0, 0)
        self.top = QWidget(self.left_menu)
        self.top.setObjectName(u"top")
        self.top.setMinimumSize(QSize(0, 60))
        self.top_menu_layout = QVBoxLayout(self.top)
        self.top_menu_layout.setSpacing(5)
        self.top_menu_layout.setObjectName(u"top_menu_layout")
        self.top_menu_layout.setContentsMargins(0, 5, 0, 0)

        self.left_menu_layout.addWidget(self.top)

        self.menu_spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.left_menu_layout.addItem(self.menu_spacer)

        self.bottom = QWidget(self.left_menu)
        self.bottom.setObjectName(u"bottom")
        self.bottom.setMinimumSize(QSize(0, 45))
        self.bottom_menu_layout = QVBoxLayout(self.bottom)
        self.bottom_menu_layout.setSpacing(2)
        self.bottom_menu_layout.setObjectName(u"bottom_menu_layout")
        self.bottom_menu_layout.setContentsMargins(0, 0, 0, 30)

        self.left_menu_layout.addWidget(self.bottom)


        self.app_layout.addWidget(self.left_menu)

        self.container = QFrame(self.app_frame)
        self.container.setObjectName(u"container")
        self.container.setFrameShape(QFrame.NoFrame)
        self.container.setFrameShadow(QFrame.Raised)
        self.content_layout = QVBoxLayout(self.container)
        self.content_layout.setSpacing(0)
        self.content_layout.setObjectName(u"content_layout")
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.pages_container = QFrame(self.container)
        self.pages_container.setObjectName(u"pages_container")
        self.pages_container.setFrameShape(QFrame.NoFrame)
        self.pages_container.setFrameShadow(QFrame.Raised)
        self.verticalLayout = QVBoxLayout(self.pages_container)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.app_pages = QStackedWidget(self.pages_container)
        self.app_pages.setObjectName(u"app_pages")
        self.app_pages.setStyleSheet(u"background: transparent;")
        self.page_orders = QWidget()
        self.page_orders.setObjectName(u"page_orders")
        self.verticalLayout_2 = QVBoxLayout(self.page_orders)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.orders_horizontal_layout = QHBoxLayout()
        self.orders_horizontal_layout.setObjectName(u"orders_horizontal_layout")

        self.verticalLayout_2.addLayout(self.orders_horizontal_layout)

        self.orders_horizontal_layout_1 = QHBoxLayout()
        self.orders_horizontal_layout_1.setObjectName(u"orders_horizontal_layout_1")

        self.verticalLayout_2.addLayout(self.orders_horizontal_layout_1)

        self.app_pages.addWidget(self.page_orders)
        self.page_file_select = QWidget()
        self.page_file_select.setObjectName(u"page_file_select")
        self.verticalLayout_6 = QVBoxLayout(self.page_file_select)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.file_select_layout = QVBoxLayout()
        self.file_select_layout.setObjectName(u"file_select_layout")

        self.verticalLayout_6.addLayout(self.file_select_layout)

        self.app_pages.addWidget(self.page_file_select)
        self.page_employees_file_select = QWidget()
        self.page_employees_file_select.setObjectName(u"page_employees_file_select")
        self.verticalLayout_8 = QVBoxLayout(self.page_employees_file_select)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.employees_file_layout = QVBoxLayout()
        self.employees_file_layout.setObjectName(u"employees_file_layout")

        self.verticalLayout_8.addLayout(self.employees_file_layout)

        self.app_pages.addWidget(self.page_employees_file_select)
        self.page_compare_file_select = QWidget()
        self.page_compare_file_select.setObjectName(u"page_compare_file_select")
        self.verticalLayout_7 = QVBoxLayout(self.page_compare_file_select)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.compare_file_layout = QVBoxLayout()
        self.compare_file_layout.setObjectName(u"compare_file_layout")

        self.verticalLayout_7.addLayout(self.compare_file_layout)

        self.app_pages.addWidget(self.page_compare_file_select)
        self.page_finances = QWidget()
        self.page_finances.setObjectName(u"page_finances")
        self.verticalLayout_3 = QVBoxLayout(self.page_finances)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.finances_horizontal_layout = QHBoxLayout()
        self.finances_horizontal_layout.setObjectName(u"finances_horizontal_layout")

        self.verticalLayout_3.addLayout(self.finances_horizontal_layout)

        self.finances_horizontal_layout_1 = QHBoxLayout()
        self.finances_horizontal_layout_1.setObjectName(u"finances_horizontal_layout_1")

        self.verticalLayout_3.addLayout(self.finances_horizontal_layout_1)

        self.app_pages.addWidget(self.page_finances)
        self.page_employees = QWidget()
        self.page_employees.setObjectName(u"page_employees")
        self.verticalLayout_5 = QVBoxLayout(self.page_employees)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.employees_horizontal_layout = QHBoxLayout()
        self.employees_horizontal_layout.setObjectName(u"employees_horizontal_layout")

        self.verticalLayout_5.addLayout(self.employees_horizontal_layout)

        self.employees_horizontal_layout_1 = QHBoxLayout()
        self.employees_horizontal_layout_1.setObjectName(u"employees_horizontal_layout_1")

        self.verticalLayout_5.addLayout(self.employees_horizontal_layout_1)

        self.app_pages.addWidget(self.page_employees)

        self.verticalLayout.addWidget(self.app_pages)


        self.content_layout.addWidget(self.pages_container)

        self.bottom_credits = QFrame(self.container)
        self.bottom_credits.setObjectName(u"bottom_credits")
        self.bottom_credits.setMinimumSize(QSize(0, 30))
        self.bottom_credits.setMaximumSize(QSize(16777215, 30))
        self.bottom_credits.setFrameShape(QFrame.NoFrame)
        self.bottom_credits.setFrameShadow(QFrame.Raised)
        self.bottom_credits_layout = QHBoxLayout(self.bottom_credits)
        self.bottom_credits_layout.setSpacing(10)
        self.bottom_credits_layout.setObjectName(u"bottom_credits_layout")
        self.bottom_credits_layout.setContentsMargins(10, 0, 10, 0)
        self.file_path_label = QLabel(self.bottom_credits)
        self.file_path_label.setObjectName(u"file_path_label")

        self.bottom_credits_layout.addWidget(self.file_path_label)

        self.horizontalSpacer = QSpacerItem(924, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.bottom_credits_layout.addItem(self.horizontalSpacer)

        self.label_2 = QLabel(self.bottom_credits)
        self.label_2.setObjectName(u"label_2")

        self.bottom_credits_layout.addWidget(self.label_2)


        self.content_layout.addWidget(self.bottom_credits)


        self.app_layout.addWidget(self.container)


        self.verticalLayout_4.addWidget(self.app_frame)

        main_window.setCentralWidget(self.central_widget)

        self.retranslateUi(main_window)

        self.app_pages.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(main_window)
    # setupUi

    def retranslateUi(self, main_window):
        main_window.setWindowTitle(QCoreApplication.translate("main_window", u"MainWindow", None))
        self.file_path_label.setText(QCoreApplication.translate("main_window", u"No file selected.", None))
        self.label_2.setText(QCoreApplication.translate("main_window", u"v1.0.0", None))
    # retranslateUi

