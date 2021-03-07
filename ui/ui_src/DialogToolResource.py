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
        DialogToolResource.resize(213, 160)
        application_path = os.path.dirname(__file__)
        uidir = os.path.abspath(os.path.join(application_path, "../."))
        DialogToolResource.setAcceptDrops(False)
        icon = QIcon()
        icon.addFile(os.path.join(uidir, u"icons/icon-resource.png"), QSize(), QIcon.Normal, QIcon.Off)
        DialogToolResource.setWindowIcon(icon)
        self.gridLayout = QGridLayout(DialogToolResource)
        self.gridLayout.setObjectName(u"gridLayout")
        self.buttonBox = QDialogButtonBox(DialogToolResource)
        self.buttonBox.setObjectName(u"buttonBox")
        font = QFont()
        font.setPointSize(12)
        self.buttonBox.setFont(font)
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(True)

        self.gridLayout.addWidget(self.buttonBox, 2, 0, 1, 2)

        self.label = QLabel(DialogToolResource)
        self.label.setObjectName(u"label")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.spinBox = QSpinBox(DialogToolResource)
        self.spinBox.setObjectName(u"spinBox")
        self.spinBox.setFont(font)

        self.gridLayout.addWidget(self.spinBox, 0, 1, 1, 1)

        self.label_2 = QLabel(DialogToolResource)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setFont(font)
        self.label_2.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)

        self.spinBox_2 = QSpinBox(DialogToolResource)
        self.spinBox_2.setObjectName(u"spinBox_2")
        self.spinBox_2.setFont(font)

        self.gridLayout.addWidget(self.spinBox_2, 1, 1, 1, 1)


        self.retranslateUi(DialogToolResource)
        self.buttonBox.accepted.connect(DialogToolResource.accept)
        self.buttonBox.rejected.connect(DialogToolResource.reject)

        QMetaObject.connectSlotsByName(DialogToolResource)
    # setupUi

    def retranslateUi(self, DialogToolResource):
        DialogToolResource.setWindowTitle(QCoreApplication.translate("DialogToolResource", u"Config Tool Resource", None))
        self.label.setText(QCoreApplication.translate("DialogToolResource", u"Thread usage:", None))
        self.label_2.setText(QCoreApplication.translate("DialogToolResource", u"DriverObject:", None))
    # retranslateUi


