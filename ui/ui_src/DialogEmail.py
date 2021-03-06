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
        DialogEmail.resize(320, 240)
        application_path = os.path.dirname(__file__)
        uidir = os.path.abspath(os.path.join(application_path, "../."))
        icon = QIcon()
        icon.addFile(os.path.join(uidir, u"icons/icon-email-notification.png"), QSize(), QIcon.Normal, QIcon.Off)
        DialogEmail.setWindowIcon(icon)
        self.buttonBox = QDialogButtonBox(DialogEmail)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setGeometry(QRect(10, 200, 301, 32))
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.retranslateUi(DialogEmail)
        self.buttonBox.accepted.connect(DialogEmail.accept)
        self.buttonBox.rejected.connect(DialogEmail.reject)

        QMetaObject.connectSlotsByName(DialogEmail)
    # setupUi

    def retranslateUi(self, DialogEmail):
        DialogEmail.setWindowTitle(QCoreApplication.translate("DialogEmail", u"Email Config", None))
    # retranslateUi


