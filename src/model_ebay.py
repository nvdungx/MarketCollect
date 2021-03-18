import os, sys, re, json, collections, time, enum, shutil
import pathlib, asyncio
from operator import itemgetter, attrgetter, methodcaller
from collections import Counter, OrderedDict
from dataclasses import dataclass, field
from datetime import datetime
import pathlib, asyncio

from src.module_xml import *

import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

KEY_PASSWORD = b"JIRA_REPORT"
KEY_SALT = b'\x08\xa3w\xa9\xbc\x12\x8c\x14f\xc2\xc0B\xe3\x03\x08F'

class EbayClient:
  def __init__(self, _console=None):
    self.id = None
    self.cert = None
    self.OAuthToken = None
    self.devId = None
    self.reqTokenUrl = None
    self.scope = None
    self.console = _console
    self.retry_time = None
    self.__loading_client_configuration()

  def console_log(self, val:str):
    if (self.console != None):
      self.console(f"{val}")

  def __loading_client_configuration(self):
    self.__client_config = XmlDoc("ebay_client_config.xml", _console=self.console_log)
    self.__client_config.parse()
    data_dict = self.__client_config.get_dict()
    if (data_dict != None):
      self.reqTokenUrl = data_dict["CLIENT-TOKEN-URL"]
      self.productApi = data_dict["PRODUCT-API"]
      self.id = self.__decode(data_dict["INFO"]["TOOL-ID"])
      self.cert = self.__decode(data_dict["INFO"]["TOOL-CERT"])
      self.devId = self.__decode(data_dict["INFO"]["DEV-ID"])
      if (data_dict["TOKEN-MINT"] != None):
        self.OAuthToken = self.__decode(data_dict["TOKEN-MINT"])
      self.scope = data_dict["CLIENT-SCOPE"]
      self.retry_time = int(data_dict["RETRY-NUM"])

  def __encode(self, val:str):
    result = ""
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(),length=32,salt=KEY_SALT,iterations=100000,backend=default_backend())
    key = base64.urlsafe_b64encode(kdf.derive(KEY_PASSWORD))
    f = Fernet(key)
    result = f.encrypt(val.encode("utf-8"))
    result = result.decode("utf-8")
    return result

  def __decode(self, val:str):
    result = ""
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(),length=32,salt=KEY_SALT,iterations=100000,backend=default_backend())
    key = base64.urlsafe_b64encode(kdf.derive(KEY_PASSWORD))
    f = Fernet(key)
    result = f.decrypt(val.encode("utf-8"))
    result = result.decode("utf-8")
    return result

  def get_header(self):
    credential = base64.b64encode(f"{self.id}:{self.cert}".encode()).decode()
    header = {"Content-Type": "application/x-www-form-urlencoded",
              "Authorization": f"Basic {credential}"}
    return header

  def get_body(self):
    body = {"grant_type": "client_credentials",
            "scope": f"{self.scope}"}
    return body