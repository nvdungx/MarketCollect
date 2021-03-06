# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'DialogToolResource.ui'
##
## Created by: Qt User Interface Compiler version 6.0.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
import os


class Ui_DialogToolResource(object):
    def setupUi(self, DialogToolResource):
        if not DialogToolResource.objectName():
            DialogToolResource.setObjectName(u"DialogToolResource")
        DialogToolResource.resize(320, 240)
        application_path = os.path.dirname(__file__)
        uidir = os.path.abspath(os.path.join(application_path, "../."))
        DialogToolResource.setAcceptDrops(False)
        icon = QIcon()
        icon.addFile(os.path.join(uidir, u"icons/icon-resource.png"), QSize(), QIcon.Normal, QIcon.Off)
        DialogToolResource.setWindowIcon(icon)
        self.buttonBox = QDialogButtonBox(DialogToolResource)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setGeometry(QRect(10, 200, 301, 32))
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.retranslateUi(DialogToolResource)
        self.buttonBox.accepted.connect(DialogToolResource.accept)
        self.buttonBox.rejected.connect(DialogToolResource.reject)

        QMetaObject.connectSlotsByName(DialogToolResource)
    # setupUi

    def retranslateUi(self, DialogToolResource):
        DialogToolResource.setWindowTitle(QCoreApplication.translate("DialogToolResource", u"Config Tool Resource", None))
    # retranslateUi


