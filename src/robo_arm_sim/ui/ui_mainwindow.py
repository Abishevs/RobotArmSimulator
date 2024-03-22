# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.6.2
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QMainWindow, QMenuBar,
    QSizePolicy, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(1000, 756)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QSize(1000, 600))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(-1, -1, 15, -1)
        self.top_bar = QWidget(self.centralwidget)
        self.top_bar.setObjectName(u"top_bar")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.top_bar.sizePolicy().hasHeightForWidth())
        self.top_bar.setSizePolicy(sizePolicy1)
        self.top_bar.setMinimumSize(QSize(0, 40))
        self.top_bar.setMaximumSize(QSize(16777215, 40))

        self.gridLayout.addWidget(self.top_bar, 0, 0, 1, 1)

        self.bottom_menubar = QWidget(self.centralwidget)
        self.bottom_menubar.setObjectName(u"bottom_menubar")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.bottom_menubar.sizePolicy().hasHeightForWidth())
        self.bottom_menubar.setSizePolicy(sizePolicy2)
        self.bottom_menubar.setMinimumSize(QSize(0, 50))
        self.bottom_menubar.setMaximumSize(QSize(16777215, 50))

        self.gridLayout.addWidget(self.bottom_menubar, 2, 0, 1, 1)

        self.sim_container = QWidget(self.centralwidget)
        self.sim_container.setObjectName(u"sim_container")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Expanding)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.sim_container.sizePolicy().hasHeightForWidth())
        self.sim_container.setSizePolicy(sizePolicy3)
        self.sim_container.setMinimumSize(QSize(250, 250))
        self.sim_container.setMaximumSize(QSize(16777215, 800))

        self.gridLayout.addWidget(self.sim_container, 1, 0, 1, 1)

        self.right_sidebar = QWidget(self.centralwidget)
        self.right_sidebar.setObjectName(u"right_sidebar")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.right_sidebar.sizePolicy().hasHeightForWidth())
        self.right_sidebar.setSizePolicy(sizePolicy4)
        self.right_sidebar.setMinimumSize(QSize(300, 650))
        self.right_sidebar.setMaximumSize(QSize(16777215, 16777215))
        self.right_sidebar.setLayoutDirection(Qt.RightToLeft)
        self.right_sidebar.setAutoFillBackground(False)

        self.gridLayout.addWidget(self.right_sidebar, 0, 1, 3, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1000, 19))
        MainWindow.setMenuBar(self.menubar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
    # retranslateUi

