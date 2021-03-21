import os, sys, re, json, collections, time, enum
from operator import itemgetter, attrgetter, methodcaller
from collections import Counter, OrderedDict
from dataclasses import dataclass, field
from datetime import datetime
import pathlib, asyncio
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
#from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from src.model_product import *
from src.model_amazon import *
from src.module_xml import *

class AmazonApi:
  def __init__(self, _console=None, _parent=None):
    self.parent = _parent
    self.cur_dir = os.path.dirname(__file__)
    self.console = _console
    self.web_obj = [] # AmazonModel object
  def is_valid(self):
    result = True
    for wo in self.web_obj:
      result &= wo.valid_page
    return result

  def __console_log(self, val):
    if (self.console != None):
      self.console(str(val))

  def remove_driver(self):
    rm_list = []
    for _obj in self.web_obj:
      if (_obj.valid_page == False):
        _obj.driver.quit()
        rm_list.append(_obj)
    for item in rm_list:
      self.web_obj.remove(item)
  def clean_driver(self, retain_val=None):
    if (retain_val == None):
      num_remove = len(self.web_obj)
    else:
      num_remove = len(self.web_obj) - retain_val
    if (num_remove != 0):
      for _ in range(num_remove):
        try:
          self.web_obj[-1].driver.quit()
        except Exception as e:
          self.__console_log(f"[ERROR][AMAZON]: Web driver fail to close {str(e)}")
        self.web_obj.pop()

  def set_driver(self, driver_type):
    self.web_obj.append(AmazonModel(driver_type, self.console))
    return self.web_obj[-1].valid_page

  def load_landing_page(self, driver_obj:AmazonModel):
    return driver_obj.set_landing_page()

  def push_product(self, _product_list):
    num_obj = len(self.web_obj)
    counter = 0
    for obj in self.web_obj:
      obj.product_list.clear()
    for product in _product_list:
      self.web_obj[counter].product_list.append(product)
      counter += 1
      if (counter == num_obj):
        counter = 0