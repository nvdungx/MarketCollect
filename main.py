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
# import ui_src
from ui.ui_src.Dialog import *

# import module code
from src.module_amazon import *
from src.module_ebay import *

class ReportFile:
  def __init__(self):
    self.path = None
    self.wb = None
    # after complete report status set to true
    self.status = False
  
  def preview(self):
    if (self.status == True):
      if (self.path != None):
        os.system("start excel ""{0}""".format(self.path))

  def load_wb(self):
    # if report file exist
    if (os.path.exists(self.path)):
      # load workbook
      self.wb = openpyxl.load_workbook(self.path)
  def save_wb(self, _path):
    # if workbook exist
    if (self.wb != None):
      # check if target _path existed
      if (os.path.exists(_path)):
        # remove old one
        os.remove(_path)
      # check if dir existed
      elif (not os.path.exists(os.path.dirname(_path))):
        # make leaf dir and intermediate one
        os.makedirs(os.path.dirname(_path))
      else:
        pass
      self.wb.save(_path)
      self.wb.close()

class MainWindow(QMainWindow):
  def __init__(self):
    self.tool_dir = os.path.dirname(__file__)
    self.report_file = ReportFile()
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
    self.ui.btnStartStop.clicked.connect(self.handleBtnClick)

  def handleBtnClick(self):
    # timer check

    
    # start amazon module
    # self.amazon.start()
    # # start ebay module
    # self.ebay.start()
    pass

  def handleImportExcelFile(self):
    # file selection dialog from tool dir, filter xlsx
    dialog = QFileDialog(self, 'Report File', self.tool_dir, filter="*.xlsx")
    # select single existed file
    dialog.setFileMode(QFileDialog.ExistingFile)
    if dialog.exec_() == QFileDialog.Accepted:
      select_file = dialog.selectedFiles()
      self.report_file.path = select_file[0]
    pass
  def handleSaveAsExcelFile(self):
    dialog = QFileDialog(self, 'Save As..', self.tool_dir, filter='*.xlsx')
    dialog.setFileMode(QFileDialog.AnyFile)
    dialog.setNameFilter("Excel (*.xlsx)")
    if dialog.exec_() == QFileDialog.Accepted:
      select_file = dialog.selectedFiles()
      self.report_file.save_wb(select_file[0])
    pass
  
  def handlePreviewOutput(self):
    self.report_file.preview()
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

if __name__ == "__main__":

  app = QApplication(sys.argv)

  window = MainWindow()
  window.show()

  sys.exit(app.exec_())
