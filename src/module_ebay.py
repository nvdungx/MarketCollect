import os, sys, re, json, collections, time
from operator import itemgetter, attrgetter, methodcaller
from collections import Counter, OrderedDict
from dataclasses import dataclass, field
from datetime import datetime
import pathlib, asyncio
import requests
import base64
from requests.auth import HTTPBasicAuth

from src.model_product import *
from src.model_ebay import *
from src.module_xml import *

# only need to view public data(i.e. price)
# application request access token with client ID and clien secret
# get the access token
# api request with access token (expire after 7200s)

class EbayApi:
  def __init__(self, _console=None, _parent=None):
    self.parent = _parent
    self.cur_dir = os.path.dirname(__file__)
    self.console = _console
    self.clientObject = EbayClient()
    self.valid_token = False
    self.token_expired = False

  def console_log(self, val):
    if (self.console != None):
      self.console(str(val))

  def get_token(self):
    self.valid_token = False
    header = self.clientObject.get_header()
    url = self.clientObject.reqTokenUrl
    body = self.clientObject.get_body()
    r = requests.post(url, headers=header, data=body)
    for _ in range(self.clientObject.retry_time):
      if (r.status_code == 200):
        try:
          result_data = r.json()
          self.clientObject.OAuthToken = result_data["access_token"]
          self.clientObject.set_element(".//TOKEN-MINT", self.clientObject.OAuthToken, encrypt=True)
          self.clientObject.set_element(".//RETRIEVE-TIME", datetime.now().isoformat())
          self.valid_token = True
          self.token_expired = False
          break
        except Exception as e:
          self.console_log(f"[ERROR]: failed during request client token from ebay {str(e)}")
    return self.valid_token

  def is_valid(self):
    if (self.valid_token == True) and (self.token_expired == False):
      return True
    else:
      return self.get_token()

  def get_price(self, product):
    if (self.valid_token == True):
      header = {'Authorization': f"Bearer {self.clientObject.OAuthToken}"}
      item_id = (product.link.split('/'))[-1]
      url = f"{self.clientObject.productApi}{item_id}"
      for _ in range(self.clientObject.retry_time):
        try:
          r = requests.get(url, headers=header)
          if (r.status_code == 200):
            rst_data = r.json()
            product.price = rst_data["price"]["value"]
            product.name = rst_data["title"]
            product.currency = rst_data["price"]["currency"]
            if (rst_data["estimatedAvailabilities"][0]["estimatedAvailabilityStatus"] == "IN_STOCK"):
              product.status = ItemStatus.IN_STOCK
            else:
              product.status = ItemStatus.OUT_STOCK
            self.console_log(f"[EBAY]: Item {product.row_idx} id {item_id} - DONE {product.price}{product.currency}")
            break
        except Exception as e:
          self.console_log(f"[ERROR][EBAY]: Item {product.row_idx} id {item_id} - {str(e)}")
      else:
        self.console_log(f"[EBAY]: Cannot found product with ID {item_id}")
    else:
      return None
