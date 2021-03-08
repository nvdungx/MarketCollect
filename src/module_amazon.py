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


COL_EBAY_LINK = 2
COL_ITEM_TITLE = 4
COL_AMA_LINK = 5
COL_AMA_STS = 6
COL_AMA_PRICE = 8
COL_EBAY_PRICE = 7

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
  site:int
  row_idx:int
  link:str
  name:str
  price:float
  currency:str
  status:ItemStatus
  status_str:str
  multi_vendor:bool
  def __init__(self, _link="", _name="", _price=0, _cur="", _status=ItemStatus.NONE, _mul=False, _site=0, _row_idx=1):
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
    self.status_str = ""
    # if product is provided by multiple vendor
    self.multi_vendor = _mul
    # 5[ama] 2[ebay]
    self.site = _site
    self.row_idx = _row_idx


class AmazonApi:
  def __init__(self):
    self.cur_dir = os.path.dirname(__file__)
    self.options = webdriver.ChromeOptions()
    self.options.add_argument("--ignore-certificate-errors")
    self.options.add_argument("--incognito")
    # self.options.add_argument("--headless")
    # self.options.add_argument("--disable-notifications")
    self.driver = None
    pass

  def start(self):
    self.webdriver.Chrome(os.path.join(self.cur_dir, "../browserdriver/ChromeDriver88.0.4324.96_32b.exe"), chrome_options=self.options)
    self.driver.get("https://amazon.com")
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
      # a-autoid-29-announce - apply code
      if(not self.__act_click_element('//*[@id="a-autoid-29-announce"]')):
        raise Exception("WEB_DRIVER", "Failed to find amazon html element {0}".format("zip-code-continue-button"))

    # for item_idx, item in enumerate(prod_list):
    #   self.driver.get(item.link)
    #   time.sleep(0.1)
    #   # TITLE
    #   # //*/div[@id="centerCol"]/*/[@id="productTitle"]
    #   result, ele = self.__act_get_element('//*/span[@id="productTitle"]')
    #   if(not result):
    #     raise Exception("WEB_DRIVER", "Failed to find amazon html element {0}".format("product-title"))
    #   else:
    #     item.name = ele.text.strip()
    #   # PRICE
    #   #             id="a-page"/id="dp"/id="dp-container"/id="ppd"/id="centerCol"/id="desktop_unifiedPrice"(div[10])/id="unifiedPrice_feature_div"/id="price"/class="a-lineitem"(table)
    #   #                                                 id="priceblock_ourprice_row"(tr)/class="a-span12"(td[2])/id="priceblock_ourprice"
    #   # /html/body/div[2]/div[3]/div[7]/div[5]/div[4]/div[10]/div/div/table/tbody/tr/td[2]/span[1]
    #   # //*[@id="priceblock_ourprice"]
    #   result, ele = self.__act_get_element('//*/span[@id="priceblock_ourprice"]')
    #   if(not result):
    #     result, ele = self.__act_get_element('//*/span[@id="priceblock_saleprice"]')
    #     if (not result):
    #       pass
    #       # print("Failed to find amazon html element {0}".format("product-price"))
    #   if(result):
    #     item.multi_vendor = False
    #     item.status = ItemStatus.IN_STOCK
    #     temp = ele.text.strip()
    #     reg = re.match(r"([^\d\.]*)([\d\.]+)([^\d\.]*)",temp)
    #     if (reg != None):
    #       item.price = float(str(reg[2]))
    #       if(str(reg[1]).strip() != ""):
    #         item.currency = str(reg[1]).strip()
    #       elif(str(reg[3]).strip() != ""):
    #         item.currency = str(reg[1]).strip()
    #       else:
    #         print("Cannot find product currency")
    #     else:
    #       raise Exception("PROCESS", "Failed to get price from string {0}".format(temp))

    #   # ITEM OUT OF STOCK or AMAZON PLACE "Available from these sellers." span script
    #   if (not result):
    #     # /html/body/div[2]/div[2]/div[8]/div[4]/div[4]/div[19]/div[1]/span
    #     # //*[@id="availability"]/span
    #     result, ele = self.__act_get_element('//*[@id="availability"]/span')
    #     if (not result):
    #       print("Failed to find amazon html element {0}".format("product-availability"))
    #     else:
    #       # OUT OF STOCK
    #       if (ele.text.strip() == ""):
    #         item.status_str = ele.text.strip()
    #         item.status = ItemStatus.OUT_STOCK
    #         item.price = 0
    #         item.currency = "$"
    #         print("Item {0} is out of stock".format(item_idx))
    #       # Available from these sellers.
    #       else:
    #         # get price from vender offer option
    #         result = False
    #   # ITEM HAS MULTIPLE VENDOR
    #   # /html/body/div[2]/div[2]/div[9]/div[4]/div[4]/div[44]
    #   # /html/body/div[2]/div[2]/div[8]/div[4]/div[4]/div[44]/div[2]/span/a
    #   # //*[@id="olp_feature_div"]
    #   if (not result):
    #     result, ele = self.__act_get_element('//*[@id="olp_feature_div"]/div/span/a[@class="a-link-normal"]/span[@class="a-size-base a-color-price"]')
    #     if (not result):
    #       raise Exception("WEB_DRIVER", "Failed to find product price, please update the target element xpath")
    #     else:
    #       item.multi_vendor = True
    #       item.status = ItemStatus.IN_STOCK
    #       temp = ele.text.strip()
    #       reg = re.match(r"([^\d\.]*)([\d\.]+)([^\d\.]*)",temp)
    #       if (reg != None):
    #         item.price = float(str(reg[2]))
    #         if(str(reg[1]).strip() != ""):
    #           item.currency = str(reg[1]).strip()
    #         elif(str(reg[3]).strip() != ""):
    #           item.currency = str(reg[1]).strip()
    #         else:
    #           print("Cannot find product currency")
    #       else:
    #         raise Exception("PROCESS", "Failed to get price from string {0}".format(temp))
    #   if (result):
    #     print("COLLECT ITEM {0} DONE - {1}{2}".format(item_idx, item.price, item.currency))
    # self.driver.quit()


  def __act_click_element(xpath):
    try:
      wait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH,xpath))).click()
      return True
    except:
      return False
  def __act_send_data(xpath, data):
    try:
      wait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH,xpath))).send_keys(data)
      return True
    except:
      return False
  def __act_get_element(xpath):
    try:
      wait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH,xpath)))
      ele = self.driver.find_element_by_xpath(xpath)
      return True, ele
    except:
      return False, None