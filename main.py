import os, sys, re, json, collections, time, threading, copy
from operator import itemgetter, attrgetter, methodcaller
from collections import Counter, OrderedDict
from dataclasses import dataclass, field
from datetime import datetime
import pathlib, asyncio
import traceback
import xml.etree.ElementTree as xmlET

# html string
import html
from io import StringIO
from html.parser import HTMLParser

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
from PySide6.QtCore import QObject, QThread, Signal, Slot, QThreadPool, QRunnable
# import ui_src
from ui.ui_src.Dialog import *

# import module code
from src.module_amazon import *
from src.module_ebay import *
from src.module_report import *
from src.module_xml import *

import pydevd

MAX_THREAD_NUM = 10
MAX_OBJ_NUM = 3
TOKEN_EXPIRE_TIME = 7200

class MLStripper(HTMLParser):
  def __init__(self):
    super().__init__()
    self.reset()
    self.strict = False
    self.convert_charrefs= True
    self.text = StringIO()
  def handle_data(self, d):
    self.text.write(d)
  def get_data(self):
    return self.text.getvalue()

def strip_tags(html):
  s = MLStripper()
  s.feed(str(html))
  return s.get_data()

class MainWindow(QMainWindow):
  def __init__(self):
    super(MainWindow, self).__init__()
    self.ui = Ui_MainWindow()
    self.ui.setupUi(self)

    # create sub view element
    self.subViewSelDriver = DialogWebDriver(self)
    self.subViewEmail = DialogEmail(self)
    self.subViewFormula = DialogFormula(self)
    self.subViewTimer = DialogTimer(self)
    self.subViewToolResource = DialogToolResource(self)

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

    self.tPool = QThreadPool(self)
    self.tPool.setMaxThreadCount(1)
    # load tool setting
    self.tPool.start(LoadToolConfig(self))

    self.tool_dir = os.path.dirname(__file__)
    self.valid_execution = False
    self.report = ReportApi(_parent=self)
    self.amazon = AmazonApi(_parent=self)
    self.ebay = EbayApi(_parent=self)
    self.token_timer = QTimer(self)
    self.token_timer.setInterval(TOKEN_EXPIRE_TIME*1000)
    self.token_timer.setSingleShot(True)
    self.token_timer.timeout.connect(self.__handleTokenExpire)
    self.pre_paths = {"import":"", "saveas":""}
    self.toolCfg = None
    self.email_list = []
    self.countdown_timers = []
    self.ebay_count = 0
    self.amaz_count = 0
    self.ebay_completed = False
    self.amaz_completed = False

  def __handleTokenExpire(self):
    self.ebay.token_expired = True

  def handleBtnClick(self):
    self.ui.btnStartStop.setEnabled(False)
    self.ui.statusbar.showMessage("Running...")
    # self.amazon.set_driver(self.subViewSelDriver.ui.comboBox.currentText(), self.subViewToolResource.ui.sBoxDriverObjNum.value())
    self.tPool.start(StartWebDriver(self))
    # --push product to amazon--
    # if (self.amazon.is_valid()):
    #   # set web driver selection
    #   if (self.amazon.set_driver(self.subViewSelDriver.ui.comboBox.currentText())):
    #     for i in range(len(self.report.amazon_prd_list)):
    #       pass
    #   else:
    #     self.ui.plainTxtLog(f"[ERROR]: Tool missing executable file for selected driver {self.subViewSelDriver.ui.comboBox.currentText()}")
    # --push product to ebay--
    # if (self.ebay.is_valid()):
    #   if (not self.token_timer.isActive()):
    #     self.token_timer.start()
    #   for i in range(len(self.report.ebay_prd_list)):
    #     self.tPool.start(GetEbayProduct(self, i))

  @Slot(dict)
  def bgModuleCompleted(self, status:dict):
    # push data from Module to report
    if (status["job"] == "ebay-prd"):
      self.ebay_count += 1
      if (self.ebay_count == len(self.report.ebay_prd_list)):
        self.ebay_completed = True
    elif (status["job"] == "mint-token"):
      if (status["result"] == True):
        self.token_timer.start()
    elif (status["job"] == "amaz-prd"):
      if (self.amaz_count == len(self.report.amazon_prd_list)):
        self.amaz_completed = True
    elif (status["job" == "report"]):
      self.ebay_completed = False
      self.amaz_completed = False
      self.ebay_count = 0
      self.amaz_count = 0
      self.ui.btnStartStop.setEnabled(True)
    if (self.ebay_completed and self.amaz_completed):
      self.report.profit_formula = self.subViewFormula.ui.lineEditFormula.text()
      self.tPool.start(GenReport(self))

  @Slot(bool)
  def bgLoadExcelInfoCompleted(self, val:bool):
    if (val == True):
      self.ui.statusbar.showMessage("Load product information from excel completed")
      self.ui.btnStartStop.setEnabled(True)
    else:
      self.ui.statusbar.showMessage("Failed to load product information from input file")
      self.ui.plainTxtLog.appendPlainText("[ERROR][EXCEL]: Failed to load product information from input file. Please makesure it's format is correct.")
      self.ui.btnStartStop.setEnabled(False)

  @Slot(bool)
  def bgLoadToolCompleted(self, val:bool):
    if (val == True):
      self.ui.statusbar.showMessage("Load tool settings completed")
      # self.tPool.start(MintEbayToken(self))
    else:
      self.ui.statusbar.showMessage("Failed to load tool settings")

  @Slot(XmlDoc)
  def loadGUISetting(self, config):
    # gui settings from xml shall be loaded to tool value
    # value change in tool settings shall be reflect to xml file
    # execution operation shall take data from tool setting component or xml file
    if (config != None):
      self.toolCfg = config
      val = self.toolCfg.get_dict()

      # previous save path
      self.pre_paths["import"] = val["FILE"]["IMPORT-LOC"]
      self.pre_paths["saveas"] = val["FILE"]["SAVE-AS"]

      # number thread spawn
      num_thread = int(val["SETTINGS"]["TOOL-RESOURCE"]["THREAD-NUM"])
      if (num_thread > MAX_THREAD_NUM):
        num_thread = MAX_THREAD_NUM
      self.tPool.setMaxThreadCount(num_thread)
      self.subViewToolResource.ui.sBoxThreadNum.setValue(num_thread)

      # number of web driver object
      num_obj = int(val["SETTINGS"]["TOOL-RESOURCE"]["OBJECT-NUM"])
      if (num_obj > MAX_OBJ_NUM):
        num_obj = MAX_OBJ_NUM
      self.subViewToolResource.ui.sBoxDriverObjNum.setValue(num_obj)

      # formula
      formula = val["SETTINGS"]["FORMULA"]
      if (formula != None) and (formula != ""):
        self.subViewFormula.ui.lineEditFormula.setText(formula)

      # selected web driver
      idx = self.subViewSelDriver.ui.comboBox.findText(val["SETTINGS"]["SELECTED-DRIVER"])
      if (idx != -1):
        self.subViewSelDriver.ui.comboBox.setCurrentIndex(idx)

      if (val["SETTINGS"]["TIMER-LIST"] != None):
        if ("TIMER" in val["SETTINGS"]["TIMER-LIST"]):
          timer_list = val["SETTINGS"]["TIMER-LIST"]["TIMER"]
          if (timer_list != None):
            # update timer
            if not (isinstance(timer_list, list)):
              timer_list = [timer_list]
            for idx, item in enumerate(timer_list):
              self.subViewTimer.addTimer(item)
              self.addSubViewTimer(f"labelTimer{idx}", item)

      if (val["SETTINGS"]["EMAIL-LIST"] != None):
        if ("EMAIL" in val["SETTINGS"]["EMAIL-LIST"]):
          email_list = val["SETTINGS"]["EMAIL-LIST"]["EMAIL"]
          if (email_list != None):
            # update email
            if not (isinstance(email_list, list)):
              email_list = [email_list]
            for item in email_list:
              self.subViewEmail.addEmail(item)
    else:
      self.ui.plainTxtLog.appendPlainText("[ERROR]: Failed to load settings")

  def handleImportExcelFile(self):
    # file selection dialog from tool dir, filter xlsx
    import_dir = self.tool_dir
    if (self.pre_paths["import"] != "") and (self.pre_paths["import"] != None):
      import_dir = self.pre_paths["import"]
    dialog = QFileDialog(self, 'Report File', import_dir, filter="*.xlsx")
    # select single existed file
    dialog.setFileMode(QFileDialog.ExistingFile)
    if dialog.exec_() == QFileDialog.Accepted:
      try:
        select_file = dialog.selectedFiles()
        if (len(select_file)>0):
          if (not self.report.set_report_file(select_file[0])):
            self.ui.statusbar.showMessage("ERROR: Invalid file path or file is not exist")
          else:
            # lunch collect product info from excel
            self.tPool.start(LoadExcelInfo(self))
            self.pre_paths["import"] = os.path.dirname(select_file[0])
            self.toolCfg.set_element(".//IMPORT-LOC", os.path.dirname(select_file[0]))
            self.toolCfg.save()
        else:
          self.ui.statusbar.showMessage("ERROR: Invalid file")
      except:
        self.ui.statusbar.showMessage("ERROR: Failed to import file")

  def handleSaveAsExcelFile(self):
    save_dir = self.tool_dir
    if ((self.pre_paths["saveas"] != "") and (self.pre_paths["saveas"] != None)):
      save_dir = self.pre_paths["saveas"]
    dialog = QFileDialog(self, 'Save As..', save_dir, filter='*.xlsx')
    dialog.setFileMode(QFileDialog.AnyFile)
    dialog.setNameFilter("Excel (*.xlsx)")
    if dialog.exec_() == QFileDialog.Accepted:
      try:
        select_file = dialog.selectedFiles()
        if (len(select_file)>0):
          if (not self.report.save_report(select_file[0])):
            self.ui.statusbar.showMessage("ERROR: Failed to save report file")
          else:
            self.pre_paths["saveas"] = os.path.dirname(select_file[0])
            self.toolCfg.set_element(".//SAVE-AS", os.path.dirname(select_file[0]))
            self.toolCfg.save()
        else:
          self.ui.statusbar.showMessage("ERROR: Invalid file path")
      except:
        self.ui.statusbar.showMessage("ERROR: Failed to save report file")

  def handlePreviewOutput(self):
    self.report.preview()
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

  def addSubViewTimer(self, label_name, count_down_val):
    labelTimer0 = QLabel(self.ui.groupBox)
    labelTimer0.setObjectName(label_name)
    font7 = QFont()
    font7.setPointSize(12)
    font7.setBold(True)
    font7.setItalic(False)
    font7.setUnderline(False)
    labelTimer0.setFont(font7)
    labelTimer0.setAlignment(Qt.AlignCenter)

    self.ui.verticalLayout.addWidget(labelTimer0)
    labelTimer0.setText(QCoreApplication.translate("MainWindow", count_down_val, None))
    self.countdown_timers.append(CountdownTimer(label_name, count_down_val, labelTimer0))

  def clearSubViewTimer(self):
    for item in self.countdown_timers:
      self.ui.verticalLayout.takeAt(0)
      item.refObj.deleteLater()
    self.countdown_timers.clear()

class CountdownTimer:
  def __init__(self, _name, _value, _refObj):
    self.refObj = _refObj
    self.name = _name
    self.value = _value

class GenReport(QRunnable):
  def __init__(self, _parent):
    super().__init__()
    self.parent = _parent
    self.signals = BackgroundSignal()
    self.signals.console.connect(self.parent.ui.plainTxtLog.appendPlainText)
    self.signals.bgwork.connect(self.parent.bgModuleCompleted)
  def console_log(self, val:str):
    self.signals.console.emit(f"{val}")
  def run(self):
    pydevd.settrace(suspend=False)
    if (self.parent.report.gen_report()):
      self.signals.bgwork.emit({"job":"report", "result":True})
    else:
      self.signals.bgwork.emit({"job":"report", "result":False})
    self.console_log("---- PRODUCT PRICE REPORT FILE GENERATION COMPLETE ----")

class GetAmazonProduct(QRunnable):
  def __init__(self, _parent):
    super().__init__()
    self.parent = _parent
    self.signals = BackgroundSignal()
    self.signals.console.connect(self.parent.ui.plainTxtLog.appendPlainText)
    self.signals.bgwork.connect(self.parent.bgModuleCompleted)
  def console_log(self, val:str):
    self.signals.console.emit(f"{val}")
  def run(self):
    pydevd.settrace(suspend=False)

    self.console_log("---- AMAZON PRODUCT PRICE COLLECT COMPLETE ----")

class StartWebDriver(QRunnable):
  def __init__(self, _parent):
    super().__init__()
    self.parent = _parent
    self.signals = BackgroundSignal()
    self.signals.bgwork.connect(self.parent.bgModuleCompleted)
    self.signals.console.connect(self.parent.ui.plainTxtLog.appendPlainText)
  def console_log(self, val:str):
    self.signals.console.emit(f"{val}")
  def run(self):
    pydevd.settrace(suspend=False)
    if (self.parent.amazon.set_driver(self.parent.subViewSelDriver.ui.comboBox.currentText(), self.parent.subViewToolResource.ui.sBoxDriverObjNum.value())):
      self.signals.bgwork.emit({"job":"amaz-landing",
                                    "result": True})
      self.signals.console.emit("[AMAZON]: Landing page successfull")
    else:
      self.signals.bgwork.emit({"job":"amaz-landing",
                                    "result": False})
      self.signals.console.emit("[AMAZON]: Landing page failed")

class MintEbayToken(QRunnable):
  def __init__(self, _parent):
    super().__init__()
    self.parent = _parent
    self.signals = BackgroundSignal()
    self.signals.console.connect(self.parent.ui.plainTxtLog.appendPlainText)
    self.signals.bgwork.connect(self.parent.bgModuleCompleted)

  def console_log(self, val:str):
    self.signals.console.emit(f"{val}")
  def run(self):
    pydevd.settrace(suspend=False)
    if (self.parent.ebay.get_token()):
      self.signals.bgwork.emit({"job":"mint-token",
                                "result": True})
      self.signals.console.emit("[EBAY]: Get client token successful")
    else:
      self.signals.console.emit("[ERROR]: Failed to get Ebay client token")
      self.signals.bgwork.emit({"job":"mint-token",
                                "result": False})

class GetEbayProduct(QRunnable):
  def __init__(self, _parent, _prd_idx):
    super().__init__()
    self.parent = _parent
    self.signals = BackgroundSignal()
    self.signals.console.connect(self.parent.ui.plainTxtLog.appendPlainText)
    self.signals.bgwork.connect(self.parent.bgModuleCompleted)
    self.prd_idx = _prd_idx
    self.parent.ebay.console = self.console_log
  def console_log(self, val:str):
    self.signals.console.emit(f"{val}")
  def run(self):
    pydevd.settrace(suspend=False)
    temp = None
    # self.console_log(f"THREAD OF PRODUCT ID {self.prd_idx} - {QThread.currentThread()}")
    temp = self.parent.ebay.get_price(self.parent.report.ebay_prd_list[self.prd_idx])
    if (temp != None):
      self.parent.report.ebay_prd_list[self.prd_idx] = temp
      self.signals.bgwork.emit({"job":"ebay-prd",
                                "result": True})
    else:
      self.signals.bgwork.emit({"job":"ebay-prd",
                                "result": False})
    self.console_log("---- EBAY PRODUCT PRICE COLLECT COMPLETE ----")

class LoadToolConfig(QRunnable):
  def __init__(self, _parent):
    super().__init__()
    self.parent = _parent
    self.signals = BackgroundSignal()
    self.signals.guisetting.connect(self.parent.loadGUISetting)
    self.signals.console.connect(self.parent.ui.plainTxtLog.appendPlainText)
    self.signals.completed.connect(self.parent.bgLoadToolCompleted)
  def console_log(self, val:str):
    self.signals.console.emit(f"{val}")
  def run(self):
    pydevd.settrace(suspend=False)
    toolCfg = XmlDoc("user_tool_setting.xml", _console=self.console_log)
    if (toolCfg.parse()):
      # return data to GUI UI
      self.signals.guisetting.emit(toolCfg)
      self.signals.completed.emit(True)
    else:
      self.signals.guisetting.emit(None)
      self.signals.completed.emit(False)

class LoadExcelInfo(QRunnable):
  def __init__(self, _parent):
    super().__init__()
    self.parent = _parent
    self.signals = BackgroundSignal()
    self.signals.completed.connect(self.parent.bgLoadExcelInfoCompleted)
    self.signals.console.connect(self.parent.ui.plainTxtLog.appendPlainText)
  def console_log(self, val:str):
    self.signals.console.emit(f"{val}")
  def run(self):
    pydevd.settrace(suspend=False)
    self.parent.report.console = self.console_log
    if (self.parent.report.get_prd_link()):
      self.signals.completed.emit(True)
    else:
      self.signals.completed.emit(False)
    self.parent.report.console = None

# Signals must inherit QObject
class BackgroundSignal(QObject):
  console = Signal(str)
  completed = Signal(bool)
  guisetting = Signal(XmlDoc)
  bgwork = Signal(dict)

if __name__ == "__main__":
  app = QApplication(sys.argv)
  window = MainWindow()
  window.show()
  sys.exit(app.exec_())
