from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
import os
import PySide6.QtCore
# import ui_src
from ui.ui_src.DialogWebDriverSelect import *
from ui.ui_src.MarketCollect import *

#define operation of Dialog SubView here
class DialogWebDriver(QDialog):
  def __init__(self):
    super().__init__()
    self.ui = Ui_DialogWebDriver()
    self.ui.setupUi(self)