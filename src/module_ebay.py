import os, sys, re, json, collections, time
from operator import itemgetter, attrgetter, methodcaller
from collections import Counter, OrderedDict
from dataclasses import dataclass, field
from datetime import datetime
import pathlib, asyncio
import openpyxl
import requests
import base64
from requests.auth import HTTPBasicAuth

from src.product import *

app_id = b"VanDungN-marketco-PRD-9dc78fcfb-e9562bf7"
dev_id = b"f930b43d-4c91-4479-bb6d-171eb4472b7c"
cert_id = b"PRD-dc78fcfbb666-d7db-4299-ab91-d553"
testval = "VanDungN-marketco-PRD-9dc78fcfb-e9562bf7:PRD-dc78fcfbb666-d7db-4299-ab91-d553"
testval2 = "VanDungN-marketco-SBX-9dc6cc39b-1c31c76b:SBX-dc6cc39b1189-0c9a-40b9-af23-b50d"
class EbayApi:
  def __init__(self):
    self.cur_dir = os.path.dirname(__file__)
    self.token = ''
    self.refresh_token = ''
    self.console = None

  def get_token(self):
    credential = base64.b64encode(testval.encode()).decode()
    header = {"Content-Type": "application/x-www-form-urlencoded",
              "Authorization": f"Basic {credential}"}
    url = "https://api.ebay.com/identity/v1/oauth2/token"
    body = {
          "grant_type": "client_credentials",
          "scope": "https://api.ebay.com/oauth/api_scope"
        }
    r = requests.post(url, headers=header, data=body)
    if (r.status_code == 200):
      result_data = r.json()
      self.token = result_data["access_token"]

  def get_price(self, prd_list:list):
    self.get_token()
    header = {'Authorization': f"Bearer {self.token}"}
    for item in prd_list:
      item_id = (item.link.split('/'))[-1]
      url = f"https://api.ebay.com/buy/browse/v1/item/get_item_by_legacy_id?legacy_item_id={item_id}"
      r = requests.get(url, headers=header)
      if (r.status_code == 200):
        rst_data = r.json()
        item.price = rst_data["price"]["value"]
        item.name = rst_data["title"]
        item.currency = rst_data["price"]["currency"]
        if (rst_data["estimatedAvailabilities"][0]["estimatedAvailabilityStatus"] == "IN_STOCK"):
          item.status = ItemStatus.IN_STOCK
        else:
          item.status = ItemStatus.OUT_STOCK
        self.console(f"[EBAY]: Item {item.row_idx} id {item_id} - DONE {item.price}{item.currency}")
      else:
        self.console(f"[EBAY]: Cannot found product with ID {item_id}")
