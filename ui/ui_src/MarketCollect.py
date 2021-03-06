# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MarketCollect.ui'
##
## Created by: Qt User Interface Compiler version 6.0.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
import os


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.setWindowModality(Qt.ApplicationModal)
        MainWindow.resize(640, 480)
        application_path = os.path.dirname(__file__)
        uidir = os.path.abspath(os.path.join(application_path, "../."))
        icon = QIcon()
        icon.addFile(os.path.join(uidir, u"icons/icon-app.jpg"), QSize(), QIcon.Normal, QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setLayoutDirection(Qt.LeftToRight)
        MainWindow.setAutoFillBackground(False)
        self.actionImport = QAction(MainWindow)
        self.actionImport.setObjectName(u"actionImport")
        icon1 = QIcon()
        icon1.addFile(os.path.join(uidir, u"icons/icon-import.png"), QSize(), QIcon.Normal, QIcon.On)
        self.actionImport.setIcon(icon1)
        self.actionSave_As = QAction(MainWindow)
        self.actionSave_As.setObjectName(u"actionSave_As")
        icon2 = QIcon()
        icon2.addFile(os.path.join(uidir, u"icons/icon-saveas.png"), QSize(), QIcon.Normal, QIcon.On)
        self.actionSave_As.setIcon(icon2)
        self.actionView_Output = QAction(MainWindow)
        self.actionView_Output.setObjectName(u"actionView_Output")
        icon3 = QIcon()
        icon3.addFile(os.path.join(uidir, u"icons/icon-preview.png"), QSize(), QIcon.Normal, QIcon.On)
        self.actionView_Output.setIcon(icon3)
        self.actionUpdate = QAction(MainWindow)
        self.actionUpdate.setObjectName(u"actionUpdate")
        icon4 = QIcon()
        icon4.addFile(os.path.join(uidir, u"icons/icon-update.png"), QSize(), QIcon.Normal, QIcon.Off)
        self.actionUpdate.setIcon(icon4)
        self.actionLicense = QAction(MainWindow)
        self.actionLicense.setObjectName(u"actionLicense")
        icon5 = QIcon()
        icon5.addFile(os.path.join(uidir, u"icons/icon-license.png"), QSize(), QIcon.Normal, QIcon.Off)
        self.actionLicense.setIcon(icon5)
        self.actionAbout = QAction(MainWindow)
        self.actionAbout.setObjectName(u"actionAbout")
        icon6 = QIcon()
        icon6.addFile(os.path.join(uidir, u"icons/icon-about.jpg"), QSize(), QIcon.Normal, QIcon.Off)
        self.actionAbout.setIcon(icon6)
        self.actionRepeat_Timer = QAction(MainWindow)
        self.actionRepeat_Timer.setObjectName(u"actionRepeat_Timer")
        icon7 = QIcon()
        icon7.addFile(os.path.join(uidir, u"icons/icon-config-timer.png"), QSize(), QIcon.Normal, QIcon.Off)
        self.actionRepeat_Timer.setIcon(icon7)
        self.actionEmail_Notification = QAction(MainWindow)
        self.actionEmail_Notification.setObjectName(u"actionEmail_Notification")
        icon8 = QIcon()
        icon8.addFile(os.path.join(uidir, u"icons/icon-email-notification.png"), QSize(), QIcon.Normal, QIcon.Off)
        self.actionEmail_Notification.setIcon(icon8)
        self.actionProfit_Formula = QAction(MainWindow)
        self.actionProfit_Formula.setObjectName(u"actionProfit_Formula")
        icon9 = QIcon()
        icon9.addFile(os.path.join(uidir, u"icons/icon-formula.png"), QSize(), QIcon.Normal, QIcon.Off)
        self.actionProfit_Formula.setIcon(icon9)
        self.actionWeb_Browser_Driver = QAction(MainWindow)
        self.actionWeb_Browser_Driver.setObjectName(u"actionWeb_Browser_Driver")
        icon10 = QIcon()
        icon10.addFile(os.path.join(uidir, u"icons/icon-webdriver.png"), QSize(), QIcon.Normal, QIcon.Off)
        self.actionWeb_Browser_Driver.setIcon(icon10)
        self.actionResource = QAction(MainWindow)
        self.actionResource.setObjectName(u"actionResource")
        icon11 = QIcon()
        icon11.addFile(os.path.join(uidir, u"icons/icon-resource.png"), QSize(), QIcon.Normal, QIcon.Off)
        self.actionResource.setIcon(icon11)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_2 = QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.plainTxtLog = QPlainTextEdit(self.centralwidget)
        self.plainTxtLog.setObjectName(u"plainTxtLog")
        self.plainTxtLog.setReadOnly(True)

        self.gridLayout_2.addWidget(self.plainTxtLog, 1, 3, 1, 1)

        self.labelProgress = QLabel(self.centralwidget)
        self.labelProgress.setObjectName(u"labelProgress")
        font = QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setUnderline(True)
        font.setStrikeOut(False)
        self.labelProgress.setFont(font)
        self.labelProgress.setAutoFillBackground(True)
        self.labelProgress.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.labelProgress, 4, 2, 1, 1)

        self.btnStartStop = QPushButton(self.centralwidget)
        self.btnStartStop.setObjectName(u"btnStartStop")
        self.btnStartStop.setEnabled(False)
        font1 = QFont()
        font1.setBold(True)
        self.btnStartStop.setFont(font1)

        self.gridLayout_2.addWidget(self.btnStartStop, 2, 3, 1, 1)

        self.progressBar = QProgressBar(self.centralwidget)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setFont(font1)
        self.progressBar.setValue(24)
        self.progressBar.setAlignment(Qt.AlignCenter)
        self.progressBar.setTextVisible(True)
        self.progressBar.setOrientation(Qt.Horizontal)

        self.gridLayout_2.addWidget(self.progressBar, 4, 3, 1, 1)

        self.dateTimeEdit = QDateTimeEdit(self.centralwidget)
        self.dateTimeEdit.setObjectName(u"dateTimeEdit")
        self.dateTimeEdit.setAutoFillBackground(True)
        self.dateTimeEdit.setWrapping(False)
        self.dateTimeEdit.setFrame(True)
        self.dateTimeEdit.setReadOnly(True)
        self.dateTimeEdit.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.dateTimeEdit.setProperty("showGroupSeparator", False)

        self.gridLayout_2.addWidget(self.dateTimeEdit, 0, 3, 1, 1)

        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        font2 = QFont()
        font2.setPointSize(11)
        font2.setBold(True)
        font2.setItalic(False)
        font2.setUnderline(False)
        self.groupBox.setFont(font2)
        self.groupBox.setFlat(False)
        self.groupBox.setCheckable(False)
        self.verticalLayout = QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.labelTimer0 = QLabel(self.groupBox)
        self.labelTimer0.setObjectName(u"labelTimer0")
        self.labelTimer0.setFont(font2)

        self.verticalLayout.addWidget(self.labelTimer0)

        self.labelTimer1 = QLabel(self.groupBox)
        self.labelTimer1.setObjectName(u"labelTimer1")
        self.labelTimer1.setFont(font2)

        self.verticalLayout.addWidget(self.labelTimer1)

        self.labelTimer2 = QLabel(self.groupBox)
        self.labelTimer2.setObjectName(u"labelTimer2")
        self.labelTimer2.setFont(font2)

        self.verticalLayout.addWidget(self.labelTimer2)

        self.labelTimer3 = QLabel(self.groupBox)
        self.labelTimer3.setObjectName(u"labelTimer3")
        self.labelTimer3.setFont(font2)

        self.verticalLayout.addWidget(self.labelTimer3)

        self.labelTimer4 = QLabel(self.groupBox)
        self.labelTimer4.setObjectName(u"labelTimer4")
        self.labelTimer4.setFont(font2)
        self.labelTimer4.setTextFormat(Qt.AutoText)

        self.verticalLayout.addWidget(self.labelTimer4)

        self.labelTimer5 = QLabel(self.groupBox)
        self.labelTimer5.setObjectName(u"labelTimer5")
        self.labelTimer5.setFont(font2)

        self.verticalLayout.addWidget(self.labelTimer5)

        self.labelTimer6 = QLabel(self.groupBox)
        self.labelTimer6.setObjectName(u"labelTimer6")
        self.labelTimer6.setFont(font2)

        self.verticalLayout.addWidget(self.labelTimer6)

        self.labelTimer7 = QLabel(self.groupBox)
        self.labelTimer7.setObjectName(u"labelTimer7")
        self.labelTimer7.setFont(font2)

        self.verticalLayout.addWidget(self.labelTimer7)


        self.gridLayout_2.addWidget(self.groupBox, 1, 2, 1, 1, Qt.AlignHCenter)

        self.labelDateTime = QLabel(self.centralwidget)
        self.labelDateTime.setObjectName(u"labelDateTime")
        font3 = QFont()
        font3.setPointSize(11)
        font3.setBold(True)
        self.labelDateTime.setFont(font3)
        self.labelDateTime.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.labelDateTime, 0, 2, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 640, 21))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuSetting = QMenu(self.menubar)
        self.menuSetting.setObjectName(u"menuSetting")
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName(u"menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuSetting.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menuFile.addAction(self.actionImport)
        self.menuFile.addAction(self.actionSave_As)
        self.menuFile.addAction(self.actionView_Output)
        self.menuSetting.addAction(self.actionRepeat_Timer)
        self.menuSetting.addAction(self.actionEmail_Notification)
        self.menuSetting.addAction(self.actionProfit_Formula)
        self.menuSetting.addAction(self.actionWeb_Browser_Driver)
        self.menuSetting.addAction(self.actionResource)
        self.menuHelp.addAction(self.actionUpdate)
        self.menuHelp.addAction(self.actionLicense)
        self.menuHelp.addAction(self.actionAbout)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MarketCollect", None))
        self.actionImport.setText(QCoreApplication.translate("MainWindow", u"Import", None))
#if QT_CONFIG(tooltip)
        self.actionImport.setToolTip(QCoreApplication.translate("MainWindow", u"Import product list file", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.actionImport.setStatusTip(QCoreApplication.translate("MainWindow", u"Import product list file", None))
#endif // QT_CONFIG(statustip)
#if QT_CONFIG(shortcut)
        self.actionImport.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+O", None))
#endif // QT_CONFIG(shortcut)
        self.actionSave_As.setText(QCoreApplication.translate("MainWindow", u"Save As...", None))
#if QT_CONFIG(tooltip)
        self.actionSave_As.setToolTip(QCoreApplication.translate("MainWindow", u"Save Completed Output File As", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.actionSave_As.setStatusTip(QCoreApplication.translate("MainWindow", u"Save Completed Output File As", None))
#endif // QT_CONFIG(statustip)
#if QT_CONFIG(shortcut)
        self.actionSave_As.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+S", None))
#endif // QT_CONFIG(shortcut)
        self.actionView_Output.setText(QCoreApplication.translate("MainWindow", u"View Output", None))
#if QT_CONFIG(tooltip)
        self.actionView_Output.setToolTip(QCoreApplication.translate("MainWindow", u"View Output of completed File", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.actionView_Output.setStatusTip(QCoreApplication.translate("MainWindow", u"View Output of completed File", None))
#endif // QT_CONFIG(statustip)
#if QT_CONFIG(shortcut)
        self.actionView_Output.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+P", None))
#endif // QT_CONFIG(shortcut)
        self.actionUpdate.setText(QCoreApplication.translate("MainWindow", u"Update", None))
        self.actionLicense.setText(QCoreApplication.translate("MainWindow", u"License", None))
        self.actionAbout.setText(QCoreApplication.translate("MainWindow", u"About", None))
        self.actionRepeat_Timer.setText(QCoreApplication.translate("MainWindow", u"Repeat Timer", None))
#if QT_CONFIG(tooltip)
        self.actionRepeat_Timer.setToolTip(QCoreApplication.translate("MainWindow", u"Config timer for repeat operation", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(shortcut)
        self.actionRepeat_Timer.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+T", None))
#endif // QT_CONFIG(shortcut)
        self.actionEmail_Notification.setText(QCoreApplication.translate("MainWindow", u"Email Notification", None))
#if QT_CONFIG(tooltip)
        self.actionEmail_Notification.setToolTip(QCoreApplication.translate("MainWindow", u"Setup email list and notification condition", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(shortcut)
        self.actionEmail_Notification.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+E", None))
#endif // QT_CONFIG(shortcut)
        self.actionProfit_Formula.setText(QCoreApplication.translate("MainWindow", u"Profit Formula", None))
#if QT_CONFIG(tooltip)
        self.actionProfit_Formula.setToolTip(QCoreApplication.translate("MainWindow", u"Set Profit Formula for Output File", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(shortcut)
        self.actionProfit_Formula.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+Q", None))
#endif // QT_CONFIG(shortcut)
        self.actionWeb_Browser_Driver.setText(QCoreApplication.translate("MainWindow", u"Select Web Driver", None))
#if QT_CONFIG(shortcut)
        self.actionWeb_Browser_Driver.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+W", None))
#endif // QT_CONFIG(shortcut)
        self.actionResource.setText(QCoreApplication.translate("MainWindow", u"Config Tool Resource", None))
#if QT_CONFIG(tooltip)
        self.actionResource.setToolTip(QCoreApplication.translate("MainWindow", u"Config Tool Resource (i.e. number of thread/core used by tool)", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(shortcut)
        self.actionResource.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+R", None))
#endif // QT_CONFIG(shortcut)
        self.labelProgress.setText(QCoreApplication.translate("MainWindow", u"Progress", None))
        self.btnStartStop.setText(QCoreApplication.translate("MainWindow", u"START", None))
        self.dateTimeEdit.setDisplayFormat(QCoreApplication.translate("MainWindow", u"dd/MM/yyyy hh:mm:ss", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"   TIMER  ", None))
        self.labelTimer0.setText(QCoreApplication.translate("MainWindow", u"00:00:00", None))
        self.labelTimer1.setText(QCoreApplication.translate("MainWindow", u"00:00:00", None))
        self.labelTimer2.setText(QCoreApplication.translate("MainWindow", u"00:00:00", None))
        self.labelTimer3.setText(QCoreApplication.translate("MainWindow", u"00:00:00", None))
        self.labelTimer4.setText(QCoreApplication.translate("MainWindow", u"00:00:00", None))
        self.labelTimer5.setText(QCoreApplication.translate("MainWindow", u"00:00:00", None))
        self.labelTimer6.setText(QCoreApplication.translate("MainWindow", u"00:00:00", None))
        self.labelTimer7.setText(QCoreApplication.translate("MainWindow", u"00:00:00", None))
        self.labelDateTime.setText(QCoreApplication.translate("MainWindow", u"DATE TIME:", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuSetting.setTitle(QCoreApplication.translate("MainWindow", u"Setting", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", u"Help", None))
    # retranslateUi


