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
from selenium.webdriver.support.ui import WebDriverWait

from src.module_xml import *
from src.model_product import *

class AmazonModel:
  def __init__(self, _driver_type, _console=None):
    self.console = _console
    self.cur_dir = os.path.dirname(__file__)
    # get match model/check type driver is match with current model
    self.driver_type = _driver_type
    self.valid_page = False
    self.page_url = None
    self.load_timeout = None
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
    self.product_list = []
    self.wait10 = None
    self.wait2 = None

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
        self.load_timeout = data_dict["LOAD-TIMEOUT"]
      else:
        self.__console_log("[ERROR][AMAZON]: Failed to load amazon page location settings")
    except Exception as e:
      self.__console_log(f"[ERROR][AMAZON]: Exception {str(e)} occur during load amazon page settings")

  def get_product_price(self):
    result = True
    self.wait10 = WebDriverWait(self.driver, 10, 0.1)
    self.wait2 = WebDriverWait(self.driver, 2, 0.1)
    for item in self.product_list:
      try:
        try:
          self.driver.get(item.link)
        except Exception as e:
          self.__console_log("[WARN][AMAZON]: Timeout page take too long to load")
        val = self.__act_get_element_text(self.product_ele["TITLE"], True, False)
        if (val != None):
          item.name = val
        else:
          self.__console_log(f"[WARN][AMAZON]: Fail to get product title")
        for k, v in self.product_ele.items():
          if (k == "TITLE"):
            continue
          else:
            if ("AVAILABILITY" in v):
              avail_sts = self.__act_get_element_text(v["AVAILABILITY"], True, False)
              if (avail_sts != None):
                if (avail_sts.upper() == "CURRENTLY UNAVAILABLE."):
                  item.status = ItemStatus.OUT_STOCK
                  item.price = 0
                  item.currency = "$"
                  item.multi_vendor = False
                  self.console("[AMAZON]: ITEM {0} UNAVAILABLE".format(item.row_idx))
                  break
                else:
                  item.status = ItemStatus.IN_STOCK
                  item.multi_vendor = True
            if ("PRICE-BLOCK" in v):
              price_val = self.__act_get_element_text(v["PRICE-BLOCK"], True, False)
              if (price_val != None):
                reg = re.match(r"([^\d\.]*)([\d\.]+)([^\d\.]*)",price_val)
                if (reg != None):
                  item.price = float(str(reg[2]))
                  if(str(reg[1]).strip() != ""):
                    item.currency = str(reg[1]).strip()
                  elif(str(reg[3]).strip() != ""):
                    item.currency = str(reg[1]).strip()
                  else:
                    # can not found currency
                    pass
                item.status = ItemStatus.IN_STOCK
                self.console("[AMAZON]: ITEM {0} DONE - {1}{2}".format(item.row_idx, item.price, item.currency))
                break
              else:
                # can not found price //*[@id="priceblock_dealprice"]
                pass
        if (item.status == ItemStatus.NONE):
          self.__console_log("[WARN][AMAZON]: Failed to get product at row {0}".format(item.row_idx))
      except Exception as e:
        self.__console_log("[WARN][AMAZON]: Exception occur during process product at row {0} - {1}".format(item.row_idx, str(e.args)))
        result = False
    return result
  def set_landing_page(self):
    self.driver.get(self.page_url)
    current_zipcode = self.__act_get_element_text(self.landing_ele["LOC-ADDR"], False, True)
    if not(self.landing_ele["ZIP-CODE-VAL"] in current_zipcode):
      action_complete = False
      if(self.__act_click_element(self.landing_ele["ZIP-CODE-BTN"], False, True)):
         if(self.__act_send_data(self.landing_ele["INPUT-BOX"], self.landing_ele["ZIP-CODE-VAL"], False, True)):
          if(self.__act_click_element(self.landing_ele["APPLY-BTN"], False, True)):
            error_text = self.__act_get_element_text('//*[@id="GLUXZipError"]/div/div/div', True, False)
            if (error_text != None):
              self.__console_log(f"[ERROR][AMAZON]: {error_text}")
              if(self.__act_click_element(self.landing_ele["DONE-BTN"], True, True)):
                action_complete = True
            else:
              if(self.__act_click_element(self.landing_ele["CONTINUE-BTN"], True, True)):
                action_complete = True
      if (action_complete == True):
        # wait for page to reload
        time.sleep(float(self.landing_ele["WAIT-ZIPCODE-CHANGE"]))
        current_zipcode = self.__act_get_element_text(self.landing_ele["LOC-ADDR"], True, False)
        self.__console_log(f"[AMAZON]: ZIPCODE {current_zipcode}")
        if (self.landing_ele["ZIP-CODE-VAL"] in current_zipcode):
          self.valid_page = True
          return True
        else:
          return False
      else:
        return False
    else:
      self.valid_page = True
    return True

  def __act_click_element(self, ele_xpath, flag=False, log_out=False):
    if (flag == False):
      wait = self.wait10
    else:
      wait = self.wait2
    try:
      wait.until(EC.visibility_of_element_located((By.XPATH, ele_xpath)), f"Failed to click element {ele_xpath}")
      self.driver.find_element_by_xpath(ele_xpath).click()
      return True
    except Exception as e:
      if (log_out == True):
        self.__console_log(f"[ERROR][AMAZON]: {e.args}")
      return False
  def __act_send_data(self, ele_xpath, data, flag=False, log_out=False):
    if (flag == False):
      wait = self.wait10
    else:
      wait = self.wait2
    try:
      wait.until(EC.visibility_of_element_located((By.XPATH, ele_xpath)), f"Failed locate element {ele_xpath}")
      self.driver.find_element_by_xpath(ele_xpath).send_keys(data)
      return True
    except Exception as e:
      if (log_out == True):
        self.__console_log(f"[ERROR][AMAZON]: {e.args}")
      return False
  def __act_get_element_text(self, ele_xpath, flag=False, log_out=False):
    if (flag == False):
      wait = self.wait10
    else:
      wait = self.wait2
    try:
      wait.until(EC.visibility_of_element_located((By.XPATH, ele_xpath)), f"Failed locate element {ele_xpath}")
      val = self.driver.find_element_by_xpath(ele_xpath).text.strip()
      return val
    except Exception as e:
      if (log_out == True):
        self.__console_log(f"[ERROR][AMAZON]: {e.args}")
      return None

  def create_new(self, _driver_type):
    self.__load_amazon_web_location(_driver_type)
    self.exe_path = os.path.abspath(os.path.join(self.cur_dir, f"../browserdriver/{_driver_type}.exe"))
    if ("ChromeDriver" in _driver_type):
      self.option = webdriver.ChromeOptions()
      self.option.add_argument("--ignore-certificate-errors")
      self.option.add_argument("--incognito")
      if (os.path.exists(self.exe_path)):
        self.driver = webdriver.Chrome(self.exe_path, chrome_options=self.option)
        self.driver.set_page_load_timeout(self.load_timeout)
        self.driver.set_script_timeout(self.load_timeout)
      else:
        self.driver = None
    elif ("FirefoxDriver" in _driver_type):
      self.option = webdriver.FirefoxOptions()
      self.option.add_argument("-turbo")
      self.option.add_argument("-browser")
      self.option.add_argument("-private")
      if (os.path.exists(self.exe_path)):
        self.driver = webdriver.Firefox(self.exe_path, chrome_options=self.option)
        self.driver.set_page_load_timeout(self.load_timeout)
        self.driver.set_script_timeout(self.load_timeout)
      else:
        self.driver = None
    elif ("MicrosoftEdge" in _driver_type):
      self.option = None
      if (os.path.exists(self.exe_path)):
        self.driver = webdriver.Edge(self.exe_path)
        self.driver.set_page_load_timeout(self.load_timeout)
        self.driver.set_script_timeout(self.load_timeout)
      else:
        self.driver = None
    if (self.driver != None):
      self.wait10 = WebDriverWait(self.driver, 10, 0.1)
      self.wait2 = WebDriverWait(self.driver, 2, 0.1)
      # load amazon home page and set landing page
      return self.set_landing_page()
    else:
      return False