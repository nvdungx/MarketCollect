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


class MainWindow(QMainWindow):
  def __init__(self):
    super(MainWindow, self).__init__()
    self.ui = Ui_MainWindow()
    self.ui.setupUi(self)

    self.subViewSelDriver = DialogWebDriver()
    # self.ui.actionWeb_Browser_Driver.connect(self.ui.actionWeb_Browser_Driver, self.ui.actionWeb_Browser_Driver.Trigger, self.__test)
    self.ui.actionWeb_Browser_Driver.triggered.connect(self.__test)

  def __test(self):
    self.subViewSelDriver.exec_()
    pass
if __name__ == "__main__":

  app = QApplication(sys.argv)

  window = MainWindow()
  window.show()

  sys.exit(app.exec_())
