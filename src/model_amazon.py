import os, sys, re, json, collections, time, enum, shutil
import pathlib, asyncio
from operator import itemgetter, attrgetter, methodcaller
from collections import Counter, OrderedDict
from dataclasses import dataclass, field
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait

from src.module_xml import *

class AmazonModel:
  def __init__(self, _driver_type, _console=None):
    self.console = _console
    self.cur_dir = os.path.dirname(__file__)
    # get match model/check type driver is match with current model
    self.driver_type = _driver_type
    self.valid_page = False
    self.page_url = None
    # struct of landing ele(zip code)
    self.landing_ele = None
    # list of product page element(pricing)
    self.product_ele = None
    self.__browser_loc = None
    # web driver
    self.option = None
    self.exe_path = os.path.abspath(os.path.join(self.cur_dir, f"../browserdriver/{_driver_type}.exe"))
    self.driver = None
    self.create_new(self.driver_type)

  def __console_log(self, val):
    if (self.console != None):
      self.console(str(val))

  def __load_amazon_web_location(self, _driver_type):
    try:
      self.__browser_loc = XmlDoc("amazon_element_location.xml", _console=self.__console_log)
      browser_tag = ""
      if ("ChromeDriver" in _driver_type):
        browser_tag = "GOOGLE-PAGE"
      elif ("FirefoxDriver" in _driver_type):
        browser_tag = "FIREFOX-PAGE"
      elif ("MicrosoftEdge" in _driver_type):
        browser_tag = "EDGE-PAGE"
      if (self.__browser_loc != None):
        self.__browser_loc.parse()
        data_dict = self.__browser_loc.get_dict()
        self.landing_ele = data_dict[browser_tag]["LANDING"]
        self.product_ele = data_dict[browser_tag]["PRODUCT"]
        self.page_url = data_dict["PAGE"]
      else:
        self.__console_log("[ERROR][AMAZON]: Failed to load amazon page location settings")
    except Exception as e:
      self.__console_log(f"[ERROR][AMAZON]: Exception {str(e)} occur during load amazon page settings")

  def __set_landing_page(self):
    self.driver.get(self.page_url)
    self.valid_page = True
    return True

  def create_new(self, _driver_type):
    self.__load_amazon_web_location(_driver_type)
    self.exe_path = os.path.abspath(os.path.join(self.cur_dir, f"../browserdriver/{_driver_type}.exe"))
    if ("ChromeDriver" in _driver_type):
      self.option = webdriver.ChromeOptions()
      self.option.add_argument("--ignore-certificate-errors")
      self.option.add_argument("--incognito")
      if (os.path.exists(self.exe_path)):
        self.driver = webdriver.Chrome(self.exe_path, chrome_options=self.option)
      else:
        self.driver = None
    elif ("FirefoxDriver" in _driver_type):
      self.option = webdriver.FirefoxOptions()
      self.option.add_argument("-turbo")
      self.option.add_argument("-browser")
      self.option.add_argument("-private")
      if (os.path.exists(self.exe_path)):
        self.driver = webdriver.Firefox(self.exe_path, chrome_options=self.option)
      else:
        self.driver = None
    elif ("MicrosoftEdge" in _driver_type):
      self.option = None
      if (os.path.exists(self.exe_path)):
        self.driver = webdriver.Edge(self.exe_path)
      else:
        self.driver = None
    if (self.driver != None):
      # load amazon home page and set landing page
      return self.__set_landing_page()
    else:
      return False