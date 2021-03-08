from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
import os, sys, shutil
import PySide6.QtCore
# import ui_src
from ui.ui_src.DialogWebDriverSelect import *
from ui.ui_src.DialogEmail import *
from ui.ui_src.DialogFormula import *
from ui.ui_src.DialogTimer import *
from ui.ui_src.DialogToolResource import *
from ui.ui_src.MarketCollect import *

#define operation of Dialog SubView here
class DialogEmail(QDialog):
  def __init__(self):
    super().__init__()
    self.ui = Ui_DialogEmail()
    self.ui.setupUi(self)

class DialogFormula(QDialog):
  def __init__(self):
    super().__init__()
    self.ui = Ui_DialogFormula()
    self.ui.setupUi(self)

class DialogTimer(QDialog):
  def __init__(self):
    super().__init__()
    self.ui = Ui_DialogTimer()
    self.ui.setupUi(self)

# self.labelTimer0 = QLabel(self.groupBox)
# self.labelTimer0.setObjectName(u"labelTimer0")
# font7 = QFont()
# font7.setPointSize(11)
# font7.setBold(False)
# font7.setItalic(False)
# font7.setUnderline(False)
# self.labelTimer0.setFont(font7)
# self.labelTimer0.setAlignment(Qt.AlignCenter)

# self.verticalLayout.addWidget(self.labelTimer0)
# self.labelTimer0.setText(QCoreApplication.translate("MainWindow", u"00:00:00", None))

class DialogToolResource(QDialog):
  def __init__(self):
    super().__init__()
    self.ui = Ui_DialogToolResource()
    self.ui.setupUi(self)

class DialogWebDriver(QDialog):
  def __init__(self):
    super().__init__()
    self.ui = Ui_DialogWebDriver()
    self.ui.setupUi(self)
    driver_dir = os.path.abspath(os.path.join(self.ui.uidir, "../browserdriver"))
    self.driver_dict = {}
    for f in os.listdir(driver_dir):
      if (os.path.isfile(os.path.join(driver_dir, f))):
        temp = str(f).replace(".exe","")
        self.driver_dict[temp] = os.path.join(driver_dir, f)
        self.ui.comboBox.addItem(temp)
    if (len(self.driver_dict) > 0):
      temp = os.listdir(driver_dir)[0].replace(".exe","")
      self.ui.comboBox.setCurrentText(QCoreApplication.translate("DialogWebDriver", temp, None))