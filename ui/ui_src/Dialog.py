import re
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
  def __init__(self, _parent):
    super().__init__()
    self.ui = Ui_DialogEmail()
    self.ui.setupUi(self)
    self.parent = _parent
    self.ui.btnAdd.clicked.connect(self.__handleAdd)
    self.ui.btnRemove.clicked.connect(self.__handleRemove)
    self.ui.listWidgetEmail.setSortingEnabled(False)
    self.ui.listWidgetEmail.setSelectionMode(QAbstractItemView.MultiSelection)
    self.add_list = []
    self.remove_list = []

  def __handleAdd(self):
    self.add_list.append(self.addEmail("sample@gmail.com"))

  def __handleRemove(self):
    self.removeEmail()

  def exec_(self):
    # load data from xml (load 1 in init)
    super().exec_()
    pass

  def addEmail(self, value=""):
    value = value.strip()
    newEmail = None
    if (re.match(r"^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$", value) != None):
      newEmail = QListWidgetItem(self.ui.listWidgetEmail)
      newEmail.setFlags(Qt.ItemIsSelectable|Qt.ItemIsEditable|Qt.ItemIsDragEnabled|Qt.ItemIsUserCheckable|Qt.ItemIsEnabled|Qt.ItemIsDropEnabled)
      newEmail.setText(value)
      self.ui.listWidgetEmail.addItem(newEmail)
    return newEmail

  def removeEmail(self):
    # get selected item, remove
    item_list = self.ui.listWidgetEmail.selectedItems()
    for item in item_list:
      if (item in self.add_list):
        self.add_list.remove(item)
      self.remove_list.append(item)
      self.ui.listWidgetEmail.takeItem(self.ui.listWidgetEmail.row(item))

  def accept(self):
    temp = []
    for idx in range(self.ui.listWidgetEmail.count()):
      temp.append(self.ui.listWidgetEmail.item(idx).text())
    # push data to xml
    self.parent.toolCfg.set_element(".//EMAIL-LIST", "EMAIL", temp)
    super().accept()
    pass

  def reject(self):
    # clean added_list
    for item in self.add_list:
      self.ui.listWidgetEmail.takeItem(self.ui.listWidgetEmail.row(item))
    for item in self.remove_list:
      self.ui.listWidgetEmail.addItem(item)
    self.add_list.clear()
    self.remove_list.clear()
    super().reject()
    pass

class DialogTimer(QDialog):
  def __init__(self, _parent):
    super().__init__()
    self.ui = Ui_DialogTimer()
    self.ui.setupUi(self)
    self.parent = _parent
    self.ui.btnAdd.clicked.connect(self.__handleAdd)
    self.ui.btnRemove.clicked.connect(self.__handleRemove)
    self.ui.listWidgetTimer.setSortingEnabled(False)
    self.ui.listWidgetTimer.setSelectionMode(QAbstractItemView.MultiSelection)

  def __handleAdd(self):
    self.addTimer("00:00:00")

  def __handleRemove(self):
    self.removeTimer()

  def exec_(self):
    # load data from xml
    super().exec_()
    pass

  def addTimer(self, value=""):
    value = value.strip()
    if (re.match(r"\d{1,2}:[0-5]?[0-9]:[0-5]?[0-9]", value) != None):
      newTimer = QListWidgetItem(self.ui.listWidgetTimer)
      newTimer.setFlags(Qt.ItemIsSelectable|Qt.ItemIsEditable|Qt.ItemIsDragEnabled|Qt.ItemIsUserCheckable|Qt.ItemIsEnabled|Qt.ItemIsDropEnabled)
      newTimer.setText(value)
      self.ui.listWidgetTimer.addItem(newTimer)

  def removeTimer(self):
    # get selected item, remove
    item_list = self.ui.listWidgetTimer.selectedIndexes()
    for item in item_list:
      self.ui.listWidgetTimer.takeItem(item.row())

  def accept(self):
    for idx in range(self.ui.listWidgetTimer.count()):
      pass
    super().accept()
    pass

  def reject(self):
    super().reject()
    pass

  # def __addSubViewTimer(self):
  #   self.labelTimer0 = QLabel(self.groupBox)
  #   self.labelTimer0.setObjectName(u"labelTimer0")
  #   font7 = QFont()
  #   font7.setPointSize(11)
  #   font7.setBold(False)
  #   font7.setItalic(False)
  #   font7.setUnderline(False)
  #   self.labelTimer0.setFont(font7)
  #   self.labelTimer0.setAlignment(Qt.AlignCenter)

  #   self.verticalLayout.addWidget(self.labelTimer0)
  #   self.labelTimer0.setText(QCoreApplication.translate("MainWindow", u"00:00:00", None))
  #   pass

class DialogFormula(QDialog):
  def __init__(self, _parent):
    super().__init__()
    self.ui = Ui_DialogFormula()
    self.ui.setupUi(self)
    self.parent = _parent

  def accept(self):
    self.parent.toolCfg.set_element(".//FORMULA", self.ui.lineEditFormula.text())
    self.parent.toolCfg.save()
    super().accept()
    pass

  def reject(self):
    super().reject()
    pass

class DialogToolResource(QDialog):
  def __init__(self, _parent):
    super().__init__()
    self.ui = Ui_DialogToolResource()
    self.ui.setupUi(self)
    self.parent = _parent
  def accept(self):
    self.parent.toolCfg.set_element(".//THREAD-NUM", self.ui.sBoxThreadNum.text())
    self.parent.toolCfg.set_element(".//OBJECT-NUM", self.ui.sBoxDriverObjNum.text())
    self.parent.toolCfg.save()
    super().accept()
    pass

  def reject(self):
    super().reject()
    pass

class DialogWebDriver(QDialog):
  def __init__(self, _parent):
    super().__init__()
    self.ui = Ui_DialogWebDriver()
    self.ui.setupUi(self)
    self.parent = _parent
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

  def accept(self):
    self.parent.toolCfg.set_element(".//SELECTED-DRIVER", self.ui.comboBox.currentText())
    self.parent.toolCfg.save()
    super().accept()

  def reject(self):
    super().reject()
    pass
