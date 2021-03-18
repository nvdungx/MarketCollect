import os, sys, re, json, collections, time, enum, shutil
import pathlib, asyncio, traceback
import xml.etree.ElementTree as ET
from operator import itemgetter, attrgetter, methodcaller
from collections import Counter, OrderedDict
from dataclasses import dataclass, field
from datetime import datetime

import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# parsing xml data file
# -> push to model amazon (amazon location)
# -> push to model ebay (ebay token)
# -> push to module report (excel location)
# -> load/save user tool setting
class XmlDoc:
  def __init__(self, _file, _console=None):
    self.console = _console
    self.dict_data = {}
    self.xmltree = None
    self.xml_root = None
    current_dir = os.path.dirname(__file__)
    if (os.path.isfile(_file) and os.path.exists(_file)):
      self.file = os.path.abspath(_file)
    elif (os.path.isfile(os.path.abspath(os.path.join(current_dir, f"../data/{_file}"))) and os.path.exists(os.path.abspath(os.path.join(current_dir, f"../data/{_file}")))):
      self.file = os.path.abspath(os.path.join(current_dir, f"../data/{_file}"))
    else:
      self.file = None

  def parse(self):
    try:
      if (self.file != None):
        self.xmltree = ET.parse(self.file)
        self.xml_root = self.xmltree.getroot()
        self.dict_data = XmlDictConfig(self.xml_root)
        return True
      else:
        return False
    except Exception as e:
      if (self.console != None):
        self.console(f"[ERROR][XML]: Failed to parse xml file {self.file} {str(e)}")
      return False

  def save(self):
    if (self.file != None):
      self.xmltree.write(self.file)

  def get_dict(self):
    # load data to dict
    if (len(self.dict_data) != 0):
      return self.dict_data
    else:
      return None

  def get_element(self, ele_tag):
    temp = self.xml_root.find(ele_tag)
    return temp.text

  def set_element(self, ele_tag, ele_val):
    if (isinstance(ele_val, str)):
      self.xml_root.find(ele_tag).text = ele_val
      return True
    else:
      return False

  def set_element_list(self, ele_tag, sub_ele_tag, sub_ele_list):
    parent_ele = self.xml_root.find(ele_tag)
    if (parent_ele != None):
      parent_text = parent_ele.tail
      parent_tail = parent_ele.tail
      parent_ele.clear()
      parent_ele.text = parent_text
      parent_ele.tail = parent_tail
      if (len(sub_ele_list) != 0):
        child_tail = parent_ele.tail+"  "
        parent_ele.text += "  "
        length = len(sub_ele_list)
        for idx, sub_ele in enumerate(sub_ele_list):
          temp = ET.Element(sub_ele_tag)
          temp.text = sub_ele
          if (idx+1 == length):
            temp.tail = parent_ele.tail
          else:
            temp.tail = child_tail
          parent_ele.append(temp)
        return True
    else:
      return False

class XmlListConfig(list):
  def __init__(self, aList):
    for element in aList:
      if element:
        # treat like dict
        if len(element) == 1 or element[0].tag != element[1].tag:
          self.append(XmlDictConfig(element))
        # treat like list
        elif element[0].tag == element[1].tag:
          self.append(XmlListConfig(element))
      elif element.text:
        text = element.text.strip()
        if text:
          self.append(text)


class XmlDictConfig(dict):
  '''
  Example usage:

  >>> tree = ElementTree.parse('your_file.xml')
  >>> root = tree.getroot()
  >>> xmldict = XmlDictConfig(root)

  Or, if you want to use an XML string:

  >>> root = ElementTree.XML(xml_string)
  >>> xmldict = XmlDictConfig(root)

  And then use xmldict for what it is... a dict.
  '''
  def __init__(self, parent_element):
    if parent_element.items():
      self.update(dict(parent_element.items()))
    for element in parent_element:
      if element:
        # treat like dict - we assume that if the first two tags
        # in a series are different, then they are all different.
        if len(element) == 1 or element[0].tag != element[1].tag:
          aDict = XmlDictConfig(element)
        # treat like list - we assume that if the first two tags
        # in a series are the same, then the rest are the same.
        else:
          # here, we put the list in dictionary; the key is the
          # tag name the list elements all share in common, and
          # the value is the list itself
          aDict = {element[0].tag: XmlListConfig(element)}
        # if the tag has attributes, add those to the dict
        if element.items():
          aDict.update(dict(element.items()))
        self.update({element.tag: aDict})
      # this assumes that if you've got an attribute in a tag,
      # you won't be having any text. This may or may not be a
      # good idea -- time will tell. It works for the way we are
      # currently doing XML configuration files...
      elif element.items():
        self.update({element.tag: dict(element.items())})
      # finally, if there are no child tags and no attributes, extract
      # the text
      else:
        self.update({element.tag: element.text})