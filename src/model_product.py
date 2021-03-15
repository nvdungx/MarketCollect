import os, sys, re, json, collections, time, enum, shutil
import pathlib, asyncio
from operator import itemgetter, attrgetter, methodcaller
from collections import Counter, OrderedDict
from dataclasses import dataclass, field
from datetime import datetime

class ItemStatus(enum.Enum):
  NONE = 1
  IN_STOCK = 2
  OUT_STOCK = 3

ITEM_STATUS = {
  ItemStatus.NONE:"NONE",
  ItemStatus.IN_STOCK:"In Stock",
  ItemStatus.OUT_STOCK:"Out of Stock"
}

@dataclass
class Product:
  link:str
  name:str
  price:float
  currency:str
  status:ItemStatus
  multi_vendor:bool
  def __init__(self, _item_num=1, _link="", _name="", _price=0, _cur="", _status=ItemStatus.NONE, _mul=False, _row_idx=1):
    # product link
    self.link = _link
    # product name
    self.name = _name
    # price value
    self.price = _price
    # currency
    self.currency = _cur
    # ItemStatus
    self.status = _status
    # if product is provided by multiple vendor
    self.multi_vendor = _mul
    # row idx(count)
    self.row_idx = _row_idx
    self.item_num = _item_num