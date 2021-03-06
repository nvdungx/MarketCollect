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
        icon = QIcon()
        icon.addFile(os.path.join(uidir, u"icons/icon-config-timer.png"), QSize(), QIcon.Normal, QIcon.Off)
        DialogTimer.setWindowIcon(icon)
        self.buttonBox = QDialogButtonBox(DialogTimer)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setGeometry(QRect(150, 10, 81, 301))
        self.buttonBox.setOrientation(Qt.Vertical)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.retranslateUi(DialogTimer)
        self.buttonBox.accepted.connect(DialogTimer.accept)
        self.buttonBox.rejected.connect(DialogTimer.reject)

        QMetaObject.connectSlotsByName(DialogTimer)
    # setupUi

    def retranslateUi(self, DialogTimer):
        DialogTimer.setWindowTitle(QCoreApplication.translate("DialogTimer", u"Timer Setting", None))
    # retranslateUi


