# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'DialogTimer.ui'
##
## Created by: Qt User Interface Compiler version 6.0.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
import os


class Ui_DialogTimer(object):
    def setupUi(self, DialogTimer):
        if not DialogTimer.objectName():
            DialogTimer.setObjectName(u"DialogTimer")
        DialogTimer.resize(240, 320)
        application_path = os.path.dirname(__file__)
        uidir = os.path.abspath(os.path.join(application_path, "../."))
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(DialogTimer.sizePolicy().hasHeightForWidth())
        DialogTimer.setSizePolicy(sizePolicy)
        icon = QIcon()
        icon.addFile(os.path.join(uidir, u"icons/icon-config-timer.png"), QSize(), QIcon.Normal, QIcon.Off)
        DialogTimer.setWindowIcon(icon)
        self.gridLayout = QGridLayout(DialogTimer)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label = QLabel(DialogTimer)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.label.setFont(font)

        self.gridLayout.addWidget(self.label, 0, 1, 1, 1)

        self.buttonBox = QDialogButtonBox(DialogTimer)
        self.buttonBox.setObjectName(u"buttonBox")
        font1 = QFont()
        font1.setPointSize(12)
        self.buttonBox.setFont(font1)
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(True)

        self.gridLayout.addWidget(self.buttonBox, 6, 1, 1, 2)

        self.frame = QFrame(DialogTimer)
        self.frame.setObjectName(u"frame")
        sizePolicy1 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy1)
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout = QVBoxLayout(self.frame)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.pushButton = QPushButton(self.frame)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setFont(font1)

        self.verticalLayout.addWidget(self.pushButton)

        self.pushButton_2 = QPushButton(self.frame)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setFont(font1)

        self.verticalLayout.addWidget(self.pushButton_2)

        self.frame_2 = QFrame(self.frame)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)

        self.verticalLayout.addWidget(self.frame_2)


        self.gridLayout.addWidget(self.frame, 4, 2, 1, 1)

        self.listWidget = QListWidget(DialogTimer)
        self.listWidget.setObjectName(u"listWidget")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.listWidget.sizePolicy().hasHeightForWidth())
        self.listWidget.setSizePolicy(sizePolicy2)
        self.listWidget.setFont(font1)

        self.gridLayout.addWidget(self.listWidget, 4, 1, 1, 1)


        self.retranslateUi(DialogTimer)
        self.buttonBox.accepted.connect(DialogTimer.accept)
        self.buttonBox.rejected.connect(DialogTimer.reject)

        QMetaObject.connectSlotsByName(DialogTimer)
    # setupUi

    def retranslateUi(self, DialogTimer):
        DialogTimer.setWindowTitle(QCoreApplication.translate("DialogTimer", u"Timer Setting", None))
        self.label.setText(QCoreApplication.translate("DialogTimer", u"Timer List", None))
        self.pushButton.setText(QCoreApplication.translate("DialogTimer", u"Add", None))
        self.pushButton_2.setText(QCoreApplication.translate("DialogTimer", u"Remove", None))
    # retranslateUi


