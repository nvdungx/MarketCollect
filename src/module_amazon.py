import os, sys, re, json, collections, time, enum
from operator import itemgetter, attrgetter, methodcaller
from collections import Counter, OrderedDict
from dataclasses import dataclass, field
from datetime import datetime
import pathlib, asyncio
import openpyxl
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
#from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from src.product import *

#LIST_TAG = [
#  '//*/span[@id="productTitle"]',
#  '//*/span[@id="priceblock_ourprice"]',
#  '//*/span[@id="priceblock_saleprice"]',
#  '//*[@id="availability"]/span',
#  '//*[@id="olp_feature_div"]/div/span/a[@class="a-link-normal"]/span[@class="a-size-base a-color-price"]'
#]
class AmazonApi:
  def __init__(self):
    self.cur_dir = os.path.dirname(__file__)
    # self.capa = DesiredCapabilities.CHROME
    # self.capa["pageLoadStrategy"] = "none"
    self.options = webdriver.ChromeOptions()
    self.options.add_argument("--ignore-certificate-errors")
    self.options.add_argument("--incognito")
    # self.options.add_argument("--headless")
    # self.options.add_argument("--disable-notifications")
    self.driver = None
    self.console = None
    pass

  # def __valid_page(self, tag_list):
  #   valid = 0
  #   for tag in tag_list:
  #     if (EC.presence_of_element_located((By.XPATH, tag))):
  #       valid += 1
  #   if (valid > 1):
  #     return True
  #   else:
  #     return False
  def get_price(self, prd_list:list):
    self.driver = webdriver.Chrome(os.path.abspath(os.path.join(self.cur_dir, "../browserdriver/ChromeDriver88.0.4324.96_32b.exe")), chrome_options=self.options)
    time.sleep(2)
    self.driver.get("https://amazon.com")
    time.sleep(1)
    # find zipcode element
    if(not self.__act_click_element('//*[@id="nav-global-location-popover-link"]')):
      raise Exception("WEB_DRIVER", "Failed to find amazon html element {0}".format("zip-code-button"))
    # //*[@id="GLUXZipUpdateInput"]
    if(not self.__act_send_data('//*[@id="GLUXZipUpdateInput"]', "97124")):
      raise Exception("WEB_DRIVER", "Failed to find amazon html element {0}".format("zip-code-textbox"))
    # GLUXZipUpdate - update code button 
    if(not self.__act_click_element('//*[@id="GLUXZipUpdate"]')):
      raise Exception("WEB_DRIVER", "Failed to find amazon html element {0}".format("zip-code-update-button"))
    # continue - GLUXConfirmAction - /html/body/div[5]/div/div/div[2]/span/span
    if (False == self.__act_click_element('//*/div[@class="a-popover-wrapper"]/div[@class="a-popover-footer"]/span/span')):
      # a-autoid-29-announce - apply code //*[@id="a-autoid-3"]/span //*[@id="a-popover-3"]/div/div[2]/span/span/span/button
      if(not self.__act_click_element('//*[@id="a-autoid-29-announce"]')):
        raise Exception("WEB_DRIVER", "Failed to find amazon html element {0}".format("zip-code-continue-button"))

    for item_idx, item in enumerate(prd_list):
      self.driver.get(item.link)
      # wait(self.driver, 20, 0.1).until(self.__valid_page(LIST_TAG))
      # self.driver.execute_script("window.stop();")
      time.sleep(0.2)
      # TITLE
      # //*/div[@id="centerCol"]/*/[@id="productTitle"]
      result, ele = self.__act_get_element('//*/span[@id="productTitle"]')
      if(not result):
        self.console("WEB_DRIVER: Failed to find amazon html element {0}".format("product-title"))
        continue
      else:
        item.name = ele.text.strip()
      # PRICE
      #             id="a-page"/id="dp"/id="dp-container"/id="ppd"/id="centerCol"/id="desktop_unifiedPrice"(div[10])/id="unifiedPrice_feature_div"/id="price"/class="a-lineitem"(table)
      #                                                 id="priceblock_ourprice_row"(tr)/class="a-span12"(td[2])/id="priceblock_ourprice"
      # /html/body/div[2]/div[3]/div[7]/div[5]/div[4]/div[10]/div/div/table/tbody/tr/td[2]/span[1]
      # //*[@id="priceblock_ourprice"]
      result, ele = self.__act_get_element('//*/span[@id="priceblock_ourprice"]')
      if(not result):
        result, ele = self.__act_get_element('//*/span[@id="priceblock_saleprice"]')
        if (not result):
          pass
          # self.console("Failed to find amazon html element {0}".format("product-price"))
      if(result):
        item.multi_vendor = False
        item.status = ItemStatus.IN_STOCK
        temp = ele.text.strip()
        reg = re.match(r"([^\d\.]*)([\d\.]+)([^\d\.]*)",temp)
        if (reg != None):
          item.price = float(str(reg[2]))
          if(str(reg[1]).strip() != ""):
            item.currency = str(reg[1]).strip()
          elif(str(reg[3]).strip() != ""):
            item.currency = str(reg[1]).strip()
          else:
            self.console("Cannot find product currency")
        else:
          self.console("PROCESS: Failed to get price from string {0}".format(temp))
          continue

      # ITEM OUT OF STOCK or AMAZON PLACE "Available from these sellers." span script
      if (not result):
        # /html/body/div[2]/div[2]/div[8]/div[4]/div[4]/div[19]/div[1]/span
        # //*[@id="availability"]/span
        result, ele = self.__act_get_element('//*[@id="availability"]/span')
        if (not result):
          self.console("Failed to find amazon html element {0}".format("product-availability"))
        else:
          # OUT OF STOCK
          if ((ele.text.strip() == "") or (ele.text.strip()=='Currently unavailable.')):
            item.status_str = ele.text.strip()
            item.status = ItemStatus.OUT_STOCK
            item.price = 0
            item.currency = "$"
            self.console("Item {0} is out of stock".format(item_idx))
          # Available from these sellers.
          else:
            # get price from vender offer option
            result = False
      # ITEM HAS MULTIPLE VENDOR
      # /html/body/div[2]/div[2]/div[9]/div[4]/div[4]/div[44]
      # /html/body/div[2]/div[2]/div[8]/div[4]/div[4]/div[44]/div[2]/span/a
      # //*[@id="olp_feature_div"]
      if (not result):
        result, ele = self.__act_get_element('//*[@id="olp_feature_div"]/div/span/a[@class="a-link-normal"]/span[@class="a-size-base a-color-price"]')
        if (not result):
          self.console("WEB_DRIVER: Failed to find product price, please update the target element xpath")
          continue
        else:
          item.multi_vendor = True
          item.status = ItemStatus.IN_STOCK
          temp = ele.text.strip()
          reg = re.match(r"([^\d\.]*)([\d\.]+)([^\d\.]*)",temp)
          if (reg != None):
            item.price = float(str(reg[2]))
            if(str(reg[1]).strip() != ""):
              item.currency = str(reg[1]).strip()
            elif(str(reg[3]).strip() != ""):
              item.currency = str(reg[1]).strip()
            else:
              self.console("Cannot find product currency")
          else:
            self.console("PROCESS: Failed to get price from string {0}".format(temp))
            continue
      if (result):
        self.console("[AMAZON]: COLLECT ITEM {0} DONE - {1}{2}".format(item_idx, item.price, item.currency))
    self.driver.quit()


  def __act_click_element(self,xpath):
    try:
      wait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH,xpath))).click()
      return True
    except:
      return False
  def __act_send_data(self,xpath, data):
    try:
      wait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH,xpath))).send_keys(data)
      return True
    except:
      return False
  def __act_get_element(self,xpath):
    try:
      wait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH,xpath)))
      ele = self.driver.find_element_by_xpath(xpath)
      return True, ele
    except:
      return False, None