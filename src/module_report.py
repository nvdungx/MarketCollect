import os, sys, re, json, collections, time, enum, shutil
from operator import itemgetter, attrgetter, methodcaller
from collections import Counter, OrderedDict
from dataclasses import dataclass, field
from datetime import datetime
import pathlib, asyncio
import openpyxl

from src.model_product import *
from src.module_xml import *

class ReportFile:
  def __init__(self):
    self.path = None
    self.wb = None
    # after complete report status set to true
    self.status = False
  
  def preview(self):
    # preview output file after operation complete
    status = False
    if (self.status == True):
      # check if valid file
      if (self.path != None):
        os.system("start excel ""{0}""".format(self.path))
        status = True
    return status

  def load_wb(self):
    # if report file exist
    if (os.path.exists(self.path)):
      # load workbook
      self.wb = openpyxl.load_workbook(self.path)
      return True
    else:
      return False

  def save_wb(self, _path=None):
    try:
      # if workbook exist
      if (self.wb != None):
        # check if target _path existed
        if (_path == None):
          # save to previous imported file
          self.wb.save(self.path)
          self.wb.close()
        else:
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
        return True
      else:
        return False
    except:
      return False

class ReportApi:
  def __init__(self):
    self.amazon_prd_list = []
    self.ebay_prd_list = []
    self.console = None
    self.__excel_location = None
    self.__start_row = 0
    self.__col_idx = 0
    self.__col = {"AMAZON-LOC":{},
                  "EBAY-LOC":{}}
    self.__report_file = ReportFile()
    self.__loading_excel_ele_location()

  def __loading_excel_ele_location(self):
    # load data from excel_element_location.xml file
    self.__excel_location = XmlDoc("excel_element_location.xml", _encrypt=False, _console=self.console)
    self.__excel_location.parse()
    data_dict = self.__excel_location.get_dict()
    self.__start_row, self.__col_idx = openpyxl.utils.coordinate_to_tuple(data_dict["INDEX-COL"])
    self.__start_row += 1
    for loc in ["AMAZON-LOC", "EBAY-LOC"]:
      coord = data_dict[loc]
      _, self.__col[loc]["LINK"] = openpyxl.utils.coordinate_to_tuple(coord["LINK"])
      _, self.__col[loc]["ITEM-TITLE"]  = openpyxl.utils.coordinate_to_tuple(coord["ITEM-TITLE"])
      _, self.__col[loc]["STATUS"]  = openpyxl.utils.coordinate_to_tuple(coord["STATUS"])
      _, self.__col[loc]["PRICE"]  = openpyxl.utils.coordinate_to_tuple(coord["PRICE"])
    pass


  def console_log(self, val:str):
    if (self.console != None):
      self.console(val)

  def set_report_file(self, file_path):
    # import report file
    # set report file path
    if (os.path.isfile(file_path)):
      _, extension = os.path.splitext(file_path)
      if (os.path.exists(os.path.abspath(file_path)) and (extension == ".xlsx")):
        self.__report_file.path = os.path.abspath(file_path)
        return True
      else:
        return False
    else:
      return False

  def preview(self):
    if(False == self.__report_file.preview()):
      self.console_log("[WARN]: Report file is not completed")

  def save_report(self, file_path=None):
    # save wb to selected file
    return self.__report_file.save_wb(file_path)

  def get_prd_link(self):
    if (self.__report_file.load_wb()):
      ws = self.__report_file.wb.active
      for row in range(self.__start_row, ws.max_row):
        for loc in ["AMAZON-LOC", "EBAY-LOC"]:
          link_val = ws.cell(row, self.__col[loc]["LINK"]).value
          item_number = ws.cell(row, self.__col_idx).value
          if ((val != None) and (val != "") and (item_number != None) and (item_number != "")):
            temp_prod = Product(_link=val,_row_idx=row, _item_num=int(item_number))
            if (loc == "AMAZON-LOC"):
              self.amazon_prd_list.append(temp_prod)
            else:
              self.ebay_prd_list.append(temp_prod)
          else:
            self.console_log(f"[WARN]: Item at row {row} missing link or SI number")
    else:
      return False

  def gen_report(self):
    ws = self.__report_file.wb.active
    for item in self.amazon_prd_list:
      ws.cell(item.row_idx, self.__col["AMAZON-LOC"]["PRICE"]).value = item.price
      ws.cell(item.row_idx, self.__col["AMAZON-LOC"]["ITEM-TITLE"]).value = item.name
      ws.cell(item.row_idx, self.__col["AMAZON-LOC"]["STATUS"]).value = ITEM_STATUS[item.status]
    for item in self.ebay_prd_list:
      ws.cell(item.row_idx, self.__col["EBAY-LOC"]["PRICE"]).value = item.price
      ws.cell(item.row_idx, self.__col["EBAY-LOC"]["ITEM-TITLE"]).value = item.name
      ws.cell(item.row_idx, self.__col["EBAY-LOC"]["STATUS"]).value = ITEM_STATUS[item.status]
    self.__report_file.save_wb()
    self.__report_file.status = True
    pass