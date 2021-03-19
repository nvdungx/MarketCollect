import re, copy
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

class JEditableListStyledItemDelegate(QStyledItemDelegate):
  # class variable for "editStarted" signal, with QModelIndex parameter
  editStarted = Signal(QModelIndex, name='editStarted')
  # class variable for "editFinished" signal, with QModelIndex parameter
  editFinished = Signal(QModelIndex, name='editFinished')

  def createEditor(self, parent: QWidget, option: QStyleOptionViewItem, index: QModelIndex):
    editor = super().createEditor(parent, option, index)
    if editor is not None:
      self.editStarted.emit(index)
    return editor

  def destroyEditor(self, editor: QWidget, index: QModelIndex):
    self.editFinished.emit(index)
    return super().destroyEditor(editor, index)

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
    self.handler = JEditableListStyledItemDelegate(self)
    self.handler.editFinished.connect(self.__validate)
    self.ui.listWidgetEmail.setItemDelegate(self.handler)
    self.current_list = []

  def __validate(self, index:QModelIndex):
    item = self.ui.listWidgetEmail.item(index.row())
    if (re.match(r"^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$", item.text()) != None):
      pass
    else:
      item.setText("sample@gmail.com")

  def __handleAdd(self):
    self.addEmail("sample@gmail.com")

  def __handleRemove(self):
    self.removeEmail()

  def exec_(self):
    # load data from xml (load 1 in init)
    for idx in range(self.ui.listWidgetEmail.count()):
      self.current_list.append(self.ui.listWidgetEmail.item(idx))
    super().exec_()

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
      self.ui.listWidgetEmail.takeItem(self.ui.listWidgetEmail.row(item))

  def accept(self):
    temp = []
    for idx in range(self.ui.listWidgetEmail.count()):
      temp.append(self.ui.listWidgetEmail.item(idx).text())
    self.parent.email_list.clear()
    self.parent.email_list.extend(temp)
    # push data to xml
    self.parent.toolCfg.set_element_list(".//EMAIL-LIST", "EMAIL", temp)
    self.parent.toolCfg.save()
    self.current_list.clear()
    super().accept()

  def reject(self):
    # clean added_list
    for _ in range(self.ui.listWidgetEmail.count()):
      self.ui.listWidgetEmail.takeItem(0)
    for item in self.current_list:
      self.ui.listWidgetEmail.addItem(item)
    self.current_list.clear()
    super().reject()

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
    self.handler = JEditableListStyledItemDelegate(self)
    self.handler.editFinished.connect(self.__validate)
    self.ui.listWidgetTimer.setItemDelegate(self.handler)
    self.current_list = []
    self.__MAX_NUM_TIMER = 10

  def __validate(self, index:QModelIndex):
    item = self.ui.listWidgetTimer.item(index.row())
    rst = re.match(r"(\d+):(\d+):(\d+)", item.text())
    if (rst != None):
      hh = "99" if (int(rst.groups()[0]) > 99) else rst.groups()[0].lstrip('0').zfill(2)
      mm = "59" if (int(rst.groups()[1]) > 59) else rst.groups()[1].lstrip('0').zfill(2)
      ss = "59" if (int(rst.groups()[2]) > 59) else rst.groups()[2].lstrip('0').zfill(2)
      val = f"{hh}:{mm}:{ss}"
      item.setText(val)
    else:
      item.setText("00:00:00")

  def __handleAdd(self):
    self.addTimer("00:00:00")

  def __handleRemove(self):
    self.removeTimer()

  def exec_(self):
    # load data current
    for idx in range(self.ui.listWidgetTimer.count()):
      self.current_list.append(self.ui.listWidgetTimer.item(idx))
    super().exec_()

  def addTimer(self, value=""):
    value = value.strip()
    newTimer = None
    if (self.ui.listWidgetTimer.count() < self.__MAX_NUM_TIMER):
      if (re.match(r"\d{1,2}:[0-5]?[0-9]:[0-5]?[0-9]", value) != None):
        newTimer = QListWidgetItem(self.ui.listWidgetTimer)
        newTimer.setFlags(Qt.ItemIsSelectable|Qt.ItemIsEditable|Qt.ItemIsDragEnabled|Qt.ItemIsUserCheckable|Qt.ItemIsEnabled|Qt.ItemIsDropEnabled)
        newTimer.setText(value)
        self.ui.listWidgetTimer.addItem(newTimer)
    return newTimer

  def removeTimer(self):
    # get selected item, remove
    item_list = self.ui.listWidgetTimer.selectedItems()
    for item in item_list:
      self.ui.listWidgetTimer.takeItem(self.ui.listWidgetTimer.row(item))

  def accept(self):
    temp = []
    self.parent.clearSubViewTimer()
    for idx in range(self.ui.listWidgetTimer.count()):
      temp.append(self.ui.listWidgetTimer.item(idx).text())
      self.parent.addSubViewTimer(f"labelTimer{idx}", self.ui.listWidgetTimer.item(idx).text())
    # push data to xml
    self.parent.toolCfg.set_element_list(".//TIMER-LIST", "TIMER", temp)
    self.parent.toolCfg.save()
    self.current_list.clear()
    super().accept()

  def reject(self):
    # clean added_list
    for _ in range(self.ui.listWidgetTimer.count()):
      self.ui.listWidgetTimer.takeItem(0)
    for item in self.current_list:
      self.ui.listWidgetTimer.addItem(item)
    self.current_list.clear()
    super().reject()

class DialogFormula(QDialog):
  def __init__(self, _parent):
    super().__init__()
    self.ui = Ui_DialogFormula()
    self.ui.setupUi(self)
    self.parent = _parent
    self.current_val = None

  def exec_(self):
    # load data from current
    self.current_val = self.ui.lineEditFormula.text()
    super().exec_()

  def accept(self):
    self.parent.toolCfg.set_element(".//FORMULA", self.ui.lineEditFormula.text())
    self.parent.toolCfg.save()
    super().accept()

  def reject(self):
    self.ui.lineEditFormula.setText(self.current_val)
    super().reject()

class DialogToolResource(QDialog):
  def __init__(self, _parent):
    super().__init__()
    self.ui = Ui_DialogToolResource()
    self.ui.setupUi(self)
    self.parent = _parent
    self.current_val = [None, None]

  def exec_(self):
    # load data from current
    self.current_val[0] = self.ui.sBoxDriverObjNum.value()
    self.current_val[1] = self.ui.sBoxThreadNum.value()
    super().exec_()

  def accept(self):
    self.parent.toolCfg.set_element(".//THREAD-NUM", self.ui.sBoxThreadNum.text())
    self.parent.toolCfg.set_element(".//OBJECT-NUM", self.ui.sBoxDriverObjNum.text())
    self.parent.toolCfg.save()
    self.parent.tPool.setMaxThreadCount(self.ui.sBoxThreadNum.value())
    super().accept()

  def reject(self):
    self.ui.sBoxDriverObjNum.setValue(self.current_val[0])
    self.ui.sBoxThreadNum.setValue(self.current_val[1])
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
    self.current_val = None
    for f in os.listdir(driver_dir):
      if (os.path.isfile(os.path.join(driver_dir, f))):
        temp = str(f).replace(".exe","")
        self.driver_dict[temp] = os.path.join(driver_dir, f)
        self.ui.comboBox.addItem(temp)
    if (len(self.driver_dict) > 0):
      temp = os.listdir(driver_dir)[0].replace(".exe","")
      self.ui.comboBox.setCurrentText(QCoreApplication.translate("DialogWebDriver", temp, None))

  def exec_(self):
    # load data from current
    self.current_val = self.ui.comboBox.currentText()
    super().exec_()

  def accept(self):
    self.parent.toolCfg.set_element(".//SELECTED-DRIVER", self.ui.comboBox.currentText())
    self.parent.toolCfg.save()
    super().accept()

  def reject(self):
    self.ui.comboBox.setCurrentText(self.current_val)
    super().reject()
    pass
