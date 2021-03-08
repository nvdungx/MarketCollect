import os, sys, re, json, collections, time, enum
from operator import itemgetter, attrgetter, methodcaller
from collections import Counter, OrderedDict
from dataclasses import dataclass, field
from datetime import datetime
import pathlib, asyncio
import openpyxl

from src.product import *

COL_EBAY_LINK = 2
COL_AMA_LINK = 5
COL_ITEM_TITLE = 4
COL_AMA_STS = 6
COL_EBAY_PRICE = 7
COL_AMA_PRICE = 8

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
  def save_wb(self, _path=None):
    # if workbook exist
    if (self.wb != None):
      # check if target _path existed
      if (_path == None):
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

class ReportApi:
  def __init__(self):
    self.amazon_prd_list = []
    self.ebay_prd_list = []
    self.report_file = ReportFile()

  def get_prd_link(self, input_file):
    self.report_file.path = input_file
    self.report_file.load_wb()
    ws = self.report_file.wb["Sheet1"]

    for row in range(2, ws.max_row):
      for col in [COL_EBAY_LINK, COL_AMA_LINK]:
        val = ws.cell(row, col).value
        if ((val != None) and (val != "")):
          temp_prod = Product(_link=val,_row_idx=row)
          if (col == COL_EBAY_LINK):
            self.ebay_prd_list.append(temp_prod)
          else:
            self.amazon_prd_list.append(temp_prod)
  
  def gen_report(self):
    ws = self.report_file.wb["Sheet1"]
    for item in self.amazon_prd_list:
      ws.cell(item.row_idx, COL_AMA_PRICE).value = item.price
      ws.cell(item.row_idx, COL_ITEM_TITLE).value = item.name
      ws.cell(item.row_idx, COL_AMA_STS).value = ITEM_STATUS[item.status]
    for item in self.ebay_prd_list:
      ws.cell(item.row_idx, COL_EBAY_PRICE).value = item.price
    self.report_file.save_wb()
    self.report_file.status = True
    pass