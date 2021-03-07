# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'DialogWebDriverSelect.ui'
##
## Created by: Qt User Interface Compiler version 6.0.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
import os


class Ui_DialogWebDriver(object):
    def setupUi(self, DialogWebDriver):
        if not DialogWebDriver.objectName():
            DialogWebDriver.setObjectName(u"DialogWebDriver")
        DialogWebDriver.resize(230, 120)
        application_path = os.path.dirname(__file__)
        uidir = os.path.abspath(os.path.join(application_path, "../."))
        icon = QIcon()
        icon.addFile(os.path.join(uidir, u"icons/icon-webdriver.png"), QSize(), QIcon.Normal, QIcon.Off)
        DialogWebDriver.setWindowIcon(icon)
        self.verticalLayout = QVBoxLayout(DialogWebDriver)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.comboBox = QComboBox(DialogWebDriver)
        self.comboBox.setObjectName(u"comboBox")
        font = QFont()
        font.setPointSize(12)
        self.comboBox.setFont(font)

        self.verticalLayout.addWidget(self.comboBox)

        self.buttonBox = QDialogButtonBox(DialogWebDriver)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setFont(font)
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(True)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(DialogWebDriver)
        self.buttonBox.accepted.connect(DialogWebDriver.accept)
        self.buttonBox.rejected.connect(DialogWebDriver.reject)

        QMetaObject.connectSlotsByName(DialogWebDriver)
    # setupUi

    def retranslateUi(self, DialogWebDriver):
        DialogWebDriver.setWindowTitle(QCoreApplication.translate("DialogWebDriver", u"Select Web Driver", None))
        self.comboBox.setCurrentText("")
    # retranslateUi


