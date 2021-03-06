# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'DialogFormula.ui'
##
## Created by: Qt User Interface Compiler version 6.0.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
import os


class Ui_DialogFormula(object):
    def setupUi(self, DialogFormula):
        if not DialogFormula.objectName():
            DialogFormula.setObjectName(u"DialogFormula")
        DialogFormula.resize(320, 240)
        application_path = os.path.dirname(__file__)
        uidir = os.path.abspath(os.path.join(application_path, "../."))
        icon = QIcon()
        icon.addFile(os.path.join(uidir, u"icons/icon-formula.png"), QSize(), QIcon.Normal, QIcon.Off)
        DialogFormula.setWindowIcon(icon)
        self.buttonBox = QDialogButtonBox(DialogFormula)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setGeometry(QRect(10, 200, 301, 32))
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.retranslateUi(DialogFormula)
        self.buttonBox.accepted.connect(DialogFormula.accept)
        self.buttonBox.rejected.connect(DialogFormula.reject)

        QMetaObject.connectSlotsByName(DialogFormula)
    # setupUi

    def retranslateUi(self, DialogFormula):
        DialogFormula.setWindowTitle(QCoreApplication.translate("DialogFormula", u"Formula Setting", None))
    # retranslateUi


