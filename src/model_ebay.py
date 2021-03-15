import os, sys, re, json, collections, time, enum, shutil
import pathlib, asyncio
from operator import itemgetter, attrgetter, methodcaller
from collections import Counter, OrderedDict
from dataclasses import dataclass, field
from datetime import datetime

class EbayClient:
  def __init__(self):
    self.id = None
    self.cert = None
    self.OAuthToken = None

  def get_header(self):
    pass

  def get_body(self):
    pass