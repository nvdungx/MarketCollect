import os, sys, re, json, collections, time
from operator import itemgetter, attrgetter, methodcaller
from collections import Counter, OrderedDict
from dataclasses import dataclass, field
from datetime import datetime
import pathlib, asyncio
import openpyxl
import requests

from src.product import *

class EbayApi:
  def __init__(self):
    self.cur_dir = os.path.dirname(__file__)
    self.token = 'v^1.1#i^1#r^0#p^1#f^0#I^3#t^H4sIAAAAAAAAAOVYa2wUVRTudttiA1hIUJSibgdNCGRm7sx0ZncHumZpeawpfbDrBjGkzONOmXbnwdw7bBdDrFUgQX8gqMEHyCOAEhNiBFQMYixIAj/gnybGRBKNRMAYNEJiDM5sl7KtpEW6wSbun82ce+653/m+c+69M6C3qnrOxiUbr00OTCjf1Qt6ywMBZiKorqqce3+wfEZlGShyCOzqfby3oi94cT6SjIwtLoPItkwEQz1GxkRi3thAuI4pWhLSkWhKBkQiVsRkfGmzyFJAtB0LW4qVIUKJpgZCUEFYC0c5XgGCEuZZz2rejJmyvHEBshxfz0WkCKcBRfDGEXJhwkRYMnEDwQKWIQFHgkiK4UWWF0GYYtjwCiKUhg7SLdNzoQARy8MV83OdIqwjQ5UQgg72ghCxRHxRsjWeaFrYkppPF8WKFXhIYgm7aOhTo6XCUFrKuHDkZVDeW0y6igIRIujYwApDg4rxm2DuAn6ealVQVC4sy4BnI3w9ZEtC5SLLMSQ8Mg7foquklncVoYl1nBuNUY8NuQsquPDU4oVINIX8v3ZXyuiaDp0GYuGC+DPxtjYilpbMJtfsbCENyemGWLHItmVNZFRVwhFN0WQSRnmBlbVwYaGBaAWah63UaJmq7pOGQi0WXgA91HA4N0wRN55Tq9nqxDXsIyr2Cw9yyK7wRR1Q0cWrTV9XaHhEhPKPoyswOBtjR5ddDAcjDB/IU9RASLatq8TwwXwtFsqnBzUQqzG2RZrOZrNUlqMsp5NmAWDo5Uubk8pqaEiE5+v3+oC/PvoEUs+nokBvJtJFnLM9LD1erXoAzE4iVs/VhzmhwPtQWLHh1n8YinKmh3ZEqTpEiQA1IvNAi3JhJqKUpENihSKlfRxQlnKFGrUzkgJJxasz14COroocr7FcRIOkKkQ1sj6qaaTMqwLJaBACCGVZiUb+T41yp6WehIoDcUlqvWR1LtsJoXVdI23HLZSbaxlJY3m3luSBkVngsF0C65jZRbysd9Lr2hvutBtun7xi2bDNyuhKrgQM+L1eQhY4R22THJxLwkzGM4wpUeQnOr5E9ucjL4Bk65Tf2JRiGbQleTu6b+rIIx5TznHbThiGiyU5AxOl2c3/o538tunp3l1nXOXk6TcgpK4OXFKovJoUWqtQDkSW63j3M6rVP7NTVjc0vR0QO1YmA500M2ah77W+fq+Pwse/PCzuLvfS3VTGU20rGd0roY7xltk9UVSXxtlpzAgMzzJhBowtr8a8pqnceDuHllgIQ3Wk1CoW3+W1mh76kh8ry/+YvsAR0Bf4sDwQADR4gpkF6qqCT1cEJ81AOoaULmkU0jtN793VgVQ3zNmS7pRXBbLTj+07XvRZYddK8NDgh4XqIDOx6CsDmHlrpJKpmT6ZZQAHIp6OPAivALNujVYwD1ZMq5s0K/J67U9fPbB5T9WW07UHNHdPG5g86BQIVJZV9AXKak7Hmpumnf3+0Jnrv9OrZp9O9++77/0ri49eyMnTm38uy05lZ05JuVfNNTdOvvJG68E9n31xOLQs23+YWPrC1p70B1Oc/jMbXv2j38CvKTe2/7k5vjL2LTlzU/ixc230kSsvfU3Kj0zNsUf3z3uz55dHZ2xZXP5Rx5q9G1rWztsdQMKmb/a9xZ54uaq/tzK6/i/q1S/3Xv6h5u1DZXVzLgu/uZJy3nzY3P5x//66k1WnKo9/+s7Byt3t/W711PZjq95dd7QL13Czdz7Z/ewn12t3ft518ar6Xao2YE7YdmlH7r2zO399TjiVPkCmjBcv9JzYUXF8241tW4MTg+fX5849v0S69ONTHfw1JxIckO9vGRZdLfARAAA='
    self.console = None

  def get_price(self, prd_list:list):
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
      