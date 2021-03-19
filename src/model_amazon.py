import os, sys, re, json, collections, time, enum, shutil
import pathlib, asyncio
from operator import itemgetter, attrgetter, methodcaller
from collections import Counter, OrderedDict
from dataclasses import dataclass, field
from datetime import datetime

class AmazonModel:
  def __init__(self):
    # get match model/check type driver is match with current model
    self.driver_type = None
    self.option = None
    self.driver_obj = None
    # struct of landing ele(zip code)
    self.landing_ele = None
    # list of product page element(pricing)
    self.product_ele = None
