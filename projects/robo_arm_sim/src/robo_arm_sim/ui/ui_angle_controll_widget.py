# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'controll_widget.ui'
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
from PySide6.QtWidgets import (QApplication, QDoubleSpinBox, QFrame, QHBoxLayout,
    QLabel, QPushButton, QSizePolicy, QSlider,
    QVBoxLayout, QWidget)

class Ui_SegmentControllWidget(object):
    def setupUi(self, SegmentControllWidget):
        if not SegmentControllWidget.objectName():
            SegmentControllWidget.setObjectName(u"SegmentControllWidget")
        SegmentControllWidget.resize(294, 210)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(SegmentControllWidget.sizePolicy().hasHeightForWidth())
        SegmentControllWidget.setSizePolicy(sizePolicy)
        SegmentControllWidget.setMinimumSize(QSize(280, 210))
        SegmentControllWidget.setMaximumSize(QSize(300, 250))
        SegmentControllWidget.setLayoutDirection(Qt.LeftToRight)
        self.verticalLayout = QVBoxLayout(SegmentControllWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, -1, 15, -1)
        self.title = QLabel(SegmentControllWidget)
        self.title.setObjectName(u"title")
        font = QFont()
        font.setPointSize(16)
        self.title.setFont(font)
        self.title.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.title)

        self.angle_label = QLabel(SegmentControllWidget)
        self.angle_label.setObjectName(u"angle_label")
        font1 = QFont()
        font1.setPointSize(12)
        self.angle_label.setFont(font1)
        self.angle_label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.verticalLayout.addWidget(self.angle_label)

        self.angle_spinbox = QDoubleSpinBox(SegmentControllWidget)
        self.angle_spinbox.setObjectName(u"angle_spinbox")

        self.verticalLayout.addWidget(self.angle_spinbox)

        self.frame = QFrame(SegmentControllWidget)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.frame)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.left_inc_btn = QPushButton(self.frame)
        self.left_inc_btn.setObjectName(u"left_inc_btn")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.left_inc_btn.sizePolicy().hasHeightForWidth())
        self.left_inc_btn.setSizePolicy(sizePolicy1)
        self.left_inc_btn.setMaximumSize(QSize(20, 20))

        self.horizontalLayout.addWidget(self.left_inc_btn)

        self.angle_slider = QSlider(self.frame)
        self.angle_slider.setObjectName(u"angle_slider")
        self.angle_slider.setMinimumSize(QSize(0, 0))
        self.angle_slider.setFont(font)
        self.angle_slider.setMinimum(-90)
        self.angle_slider.setMaximum(90)
        self.angle_slider.setSingleStep(0)
        self.angle_slider.setOrientation(Qt.Horizontal)

        self.horizontalLayout.addWidget(self.angle_slider)

        self.right_inc_btn = QPushButton(self.frame)
        self.right_inc_btn.setObjectName(u"right_inc_btn")
        sizePolicy1.setHeightForWidth(self.right_inc_btn.sizePolicy().hasHeightForWidth())
        self.right_inc_btn.setSizePolicy(sizePolicy1)
        self.right_inc_btn.setMaximumSize(QSize(20, 20))

        self.horizontalLayout.addWidget(self.right_inc_btn)


        self.verticalLayout.addWidget(self.frame)

        self.length_label = QLabel(SegmentControllWidget)
        self.length_label.setObjectName(u"length_label")
        self.length_label.setFont(font1)

        self.verticalLayout.addWidget(self.length_label)

        self.length_spinbox = QDoubleSpinBox(SegmentControllWidget)
        self.length_spinbox.setObjectName(u"length_spinbox")
        font2 = QFont()
        font2.setPointSize(9)
        self.length_spinbox.setFont(font2)

        self.verticalLayout.addWidget(self.length_spinbox)

        self.line = QFrame(SegmentControllWidget)
        self.line.setObjectName(u"line")
        self.line.setMinimumSize(QSize(0, 5))
        self.line.setSizeIncrement(QSize(0, 5))
        font3 = QFont()
        font3.setBold(False)
        self.line.setFont(font3)
        self.line.setLineWidth(2)
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line)


        self.retranslateUi(SegmentControllWidget)

        QMetaObject.connectSlotsByName(SegmentControllWidget)
    # setupUi

    def retranslateUi(self, SegmentControllWidget):
        SegmentControllWidget.setWindowTitle(QCoreApplication.translate("SegmentControllWidget", u"Form", None))
        self.title.setText(QCoreApplication.translate("SegmentControllWidget", u"Title", None))
        self.angle_label.setText(QCoreApplication.translate("SegmentControllWidget", u"Theta_1", None))
        self.left_inc_btn.setText(QCoreApplication.translate("SegmentControllWidget", u"<", None))
        self.right_inc_btn.setText(QCoreApplication.translate("SegmentControllWidget", u">", None))
        self.length_label.setText(QCoreApplication.translate("SegmentControllWidget", u"Length_1", None))
    # retranslateUi

