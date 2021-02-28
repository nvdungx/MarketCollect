import os, sys, re, json, collections
from operator import itemgetter, attrgetter, methodcaller
from collections import Counter, OrderedDict
import pathlib, asyncio
import openpyxl
from dataclasses import dataclass, field

COL_EBAY_LINK = 2
COL_ITEM_TITLE = 4
COL_AMA_LINK = 5
COL_AMA_STS = 6
COL_AMA_PRICE = 8
COL_EBAY_PRICE = 7

class ItemStatus:
  NONE = 1
  IN_STOCK = 2
  OUT_STOCK = 3

@dataclass
class Product:
  site:int
  link:str
  name:str
  price:float
  currency:str
  status:ItemStatus
  multi_vendor:bool
  def __init__(self, _link="", _name="", _price=0, _cur="", _status=ItemStatus.NONE, _mul=False, _site=0):
    self.link = _link
    self.name = _name
    self.price = _price
    self.currency = _cur
    self.status = _status
    self.multi_vendor = _mul
    self.site = _site

def get_price_ebay(prod_list):

  pass

def get_price_amazon(prod_list):

  pass

def update_excel(prod_list):

  pass

def main(args)->None:
  wb = openpyxl.load_workbook(args[1])
  ws = wb["Sheet1"]

  prod_list = {0:[], 1:[]}
  for row in range(2, ws.max_row):
    for idx, col in enumerate([COL_EBAY_LINK, COL_AMA_LINK]):
      val = ws.cell(row, col).value
      if ((val != None) and (val != "")):
        temp_prod = Product(_site=col,_link=val)
        prod_list[idx].append(temp_prod)
  
  get_price_ebay(prod_list[0])

  get_price_amazon(prod_list[1])

  update_excel(prod_list)

  pass

if __name__ == "__main__":
  main(sys.argv)