# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'DialogEmail.ui'
##
## Created by: Qt User Interface Compiler version 6.0.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
import os


class Ui_DialogEmail(object):
    def setupUi(self, DialogEmail):
        if not DialogEmail.objectName():
            DialogEmail.setObjectName(u"DialogEmail")
        DialogEmail.resize(375, 375)
        application_path = os.path.dirname(__file__)
        self.uidir = os.path.abspath(os.path.join(application_path, "../."))
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(DialogEmail.sizePolicy().hasHeightForWidth())
        DialogEmail.setSizePolicy(sizePolicy)
        icon = QIcon()
        icon.addFile(os.path.join(self.uidir, u"icons/icon-email-notification.png"), QSize(), QIcon.Normal, QIcon.Off)
        DialogEmail.setWindowIcon(icon)
        self.gridLayout = QGridLayout(DialogEmail)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label = QLabel(DialogEmail)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.label.setFont(font)

        self.gridLayout.addWidget(self.label, 0, 1, 1, 1)

        self.buttonBox = QDialogButtonBox(DialogEmail)
        self.buttonBox.setObjectName(u"buttonBox")
        font1 = QFont()
        font1.setPointSize(12)
        self.buttonBox.setFont(font1)
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(True)

        self.gridLayout.addWidget(self.buttonBox, 6, 1, 1, 2)

        self.frame = QFrame(DialogEmail)
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
        self.btnAdd = QPushButton(self.frame)
        self.btnAdd.setObjectName(u"btnAdd")
        self.btnAdd.setFont(font1)

        self.verticalLayout.addWidget(self.btnAdd)

        self.btnRemove = QPushButton(self.frame)
        self.btnRemove.setObjectName(u"btnRemove")
        self.btnRemove.setFont(font1)

        self.verticalLayout.addWidget(self.btnRemove)

        self.frame_2 = QFrame(self.frame)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)

        self.verticalLayout.addWidget(self.frame_2)


        self.gridLayout.addWidget(self.frame, 4, 2, 1, 1)

        self.listWidgetEmail = QListWidget(DialogEmail)
        self.listWidgetEmail.setObjectName(u"listWidgetEmail")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.listWidgetEmail.sizePolicy().hasHeightForWidth())
        self.listWidgetEmail.setSizePolicy(sizePolicy2)
        self.listWidgetEmail.setFont(font1)

        self.gridLayout.addWidget(self.listWidgetEmail, 4, 1, 1, 1)


        self.retranslateUi(DialogEmail)
        self.buttonBox.accepted.connect(DialogEmail.accept)
        self.buttonBox.rejected.connect(DialogEmail.reject)

        QMetaObject.connectSlotsByName(DialogEmail)
    # setupUi

    def retranslateUi(self, DialogEmail):
        DialogEmail.setWindowTitle(QCoreApplication.translate("DialogEmail", u"Email Setting", None))
        self.label.setText(QCoreApplication.translate("DialogEmail", u"Email List", None))
        self.btnAdd.setText(QCoreApplication.translate("DialogEmail", u"Add", None))
        self.btnRemove.setText(QCoreApplication.translate("DialogEmail", u"Remove", None))
    # retranslateUi
