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
        DialogFormula.resize(320, 101)
        application_path = os.path.dirname(__file__)
        self.uidir = os.path.abspath(os.path.join(application_path, "../."))
        icon = QIcon()
        icon.addFile(os.path.join(self.uidir, u"icons/icon-formula.png"), QSize(), QIcon.Normal, QIcon.Off)
        DialogFormula.setWindowIcon(icon)
        self.gridLayout = QGridLayout(DialogFormula)
        self.gridLayout.setObjectName(u"gridLayout")
        self.lineEditFormula = QLineEdit(DialogFormula)
        self.lineEditFormula.setObjectName(u"lineEditFormula")
        font = QFont()
        font.setPointSize(12)
        self.lineEditFormula.setFont(font)

        self.gridLayout.addWidget(self.lineEditFormula, 0, 1, 1, 1)

        self.label = QLabel(DialogFormula)
        self.label.setObjectName(u"label")
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.buttonBox = QDialogButtonBox(DialogFormula)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setFont(font)
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(True)

        self.gridLayout.addWidget(self.buttonBox, 2, 0, 1, 2)


        self.retranslateUi(DialogFormula)
        self.buttonBox.accepted.connect(DialogFormula.accept)
        self.buttonBox.rejected.connect(DialogFormula.reject)

        QMetaObject.connectSlotsByName(DialogFormula)
    # setupUi

    def retranslateUi(self, DialogFormula):
        DialogFormula.setWindowTitle(QCoreApplication.translate("DialogFormula", u"Formula Setting", None))
        self.label.setText(QCoreApplication.translate("DialogFormula", u"Input:", None))
    # retranslateUi


