import os, sys, re, json, collections, time, threading, copy
from operator import itemgetter, attrgetter, methodcaller
from collections import Counter, OrderedDict
from dataclasses import dataclass, field
from datetime import datetime
import pathlib, asyncio
import traceback
import xml.etree.ElementTree as xmlET

# lib for excel operation
import openpyxl

# lib for amazon selenium
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait

# lib for crypto configuration
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# lib for UI
from PySide6.QtWidgets import QApplication, QMainWindow, QDialog, QFileDialog
import PySide6.QtCore
from PySide6.QtCore import QObject, QThread, Signal, Slot
# import ui_src
from ui.ui_src.Dialog import *

# import module code
from src.module_amazon import *
from src.module_ebay import *
from src.module_report import *

import pydevd

class MainWindow(QMainWindow):
  def __init__(self):
    self.tool_dir = os.path.dirname(__file__)
    self.valid_execution = False
    self.report = ReportApi()
    self.amazon = AmazonApi()
    self.ebay = EbayApi()

    super(MainWindow, self).__init__()
    self.ui = Ui_MainWindow()
    self.ui.setupUi(self)

    # create sub view element
    self.subViewSelDriver = DialogWebDriver()
    self.subViewEmail = DialogEmail()
    self.subViewFormula = DialogFormula()
    self.subViewTimer = DialogTimer()
    self.subViewToolResource = DialogToolResource()

    # push api to get/set data from Dialog
    self.ui.actionWeb_Browser_Driver.triggered.connect(self.subViewSelDriver.exec_)
    self.ui.actionEmail_Notification.triggered.connect(self.subViewEmail.exec_)
    self.ui.actionProfit_Formula.triggered.connect(self.subViewFormula.exec_)
    self.ui.actionRepeat_Timer.triggered.connect(self.subViewTimer.exec_)
    self.ui.actionResource.triggered.connect(self.subViewToolResource.exec_)

    # link trigger action to corresponding api
    self.ui.actionImport.triggered.connect(self.handleImportExcelFile)
    self.ui.actionSave_As.triggered.connect(self.handleSaveAsExcelFile)
    self.ui.actionView_Output.triggered.connect(self.handlePreviewOutput)
    self.ui.actionUpdate.triggered.connect(self.handleToolVersionUpdate)
    self.ui.actionLicense.triggered.connect(self.handleLicenseChecking)
    self.ui.actionAbout.triggered.connect(self.handleAboutInfo)

    # start button operation
    self.ui.btnStartStop.setEnabled(False)
    self.ui.btnStartStop.clicked.connect(self.handleBtnClick)

  def handleBtnClick(self):
    self.ui.btnStartStop.setEnabled(False)
    self.ui.statusbar.showMessage("Running...")
    self.bg = BackgroundThread(self)
    self.bg.start()

  @Slot(bool)
  def bgThreadCompleted(self):
    self.ui.statusbar.showMessage("Completed", 3)
    self.ui.btnStartStop.setEnabled(True)

  def handleImportExcelFile(self):
    # file selection dialog from tool dir, filter xlsx
    dialog = QFileDialog(self, 'Report File', self.tool_dir, filter="*.xlsx")
    # select single existed file
    dialog.setFileMode(QFileDialog.ExistingFile)
    if dialog.exec_() == QFileDialog.Accepted:
      try:
        select_file = dialog.selectedFiles()
        if (len(select_file)>0):
          if (not self.report.set_report_file(select_file[0])):
            self.ui.statusbar.showMessage("ERROR: Invalid file path or file is not exist", 2)
        else:
          self.ui.statusbar.showMessage("ERROR: Invalid file", 2)
      except:
        self.ui.statusbar.showMessage("ERROR: Failed to import file", 2)

  def handleSaveAsExcelFile(self):
    dialog = QFileDialog(self, 'Save As..', self.tool_dir, filter='*.xlsx')
    dialog.setFileMode(QFileDialog.AnyFile)
    dialog.setNameFilter("Excel (*.xlsx)")
    if dialog.exec_() == QFileDialog.Accepted:
      try:
        select_file = dialog.selectedFiles()
        if (len(select_file)>0):
          if (not self.report.save_report(select_file[0])):
            self.ui.statusbar.showMessage("ERROR: Failed to save report file", 2)
        else:
          self.ui.statusbar.showMessage("ERROR: Invalid file path")
      except:
        self.ui.statusbar.showMessage("ERROR: Failed to save report file", 2)
  
  def handlePreviewOutput(self):
    self.report.report_file.preview()
    pass

  def handleToolVersionUpdate(self):
    # TODO: update Tool with new version
    pass

  def handleLicenseChecking(self):
    # TODO: tool licensing
    pass

  def handleAboutInfo(self):
    dialog = QDialog(self)
    dialog.setObjectName("dialogAbout")
    dialog.setWindowTitle("About")
    dialog.setFixedSize(320,100)
    layout = PySide6.QtWidgets.QHBoxLayout(dialog)
    labelAbout = QLabel(dialog)
    labelAbout.setObjectName(u"labelAbout")
    labelAbout.setText(
    "Amazon-Ebay product price collect tool."
    "\r\n® TGPCB LLC."
    "\r\nEmail: Sample@gmail.com")
    labelAbout.setAlignment(PySide6.QtCore.Qt.AlignCenter)
    layout.addWidget(labelAbout)
    dialog.exec_()
    pass


# Signals must inherit QObject
class BackgroundSignal(QObject):
  console = Signal(str)
  completed = Signal(bool)

class BackgroundThread(QThread):
  def __init__(self, _parent:MainWindow):
    self.parent = _parent
    QThread.__init__(self, self.parent)
    self.signals = BackgroundSignal()
    self.signals.console.connect(self.parent.ui.plainTxtLog.appendPlainText)
    self.signals.completed.connect(self.parent.bgThreadCompleted)

  def console_log(self, val:str):
    self.signals.console.emit(f"{val}")

  def run(self):
    pydevd.settrace(suspend=False)
    self.parent.amazon.console = self.console_log
    self.parent.ebay.console = self.console_log
    self.parent.report.get_prd_link(os.path.abspath(os.path.join(self.parent.tool_dir, "./data/Check-Price-AMZ-EBAY.xlsx")))
    try:
      self.parent.amazon.get_price(self.parent.report.amazon_prd_list)
    except Exception as e:
      self.console_log(str(e.args))
    try:
      self.parent.ebay.get_price(self.parent.report.ebay_prd_list)
    except Exception as e:
      self.console_log(str(e.args))
    self.parent.report.gen_report()
    self.signals.completed.emit(True)


if __name__ == "__main__":

  app = QApplication(sys.argv)

  window = MainWindow()
  window.show()

  sys.exit(app.exec_())
