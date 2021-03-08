# -*- coding: utf-8 -*-
"""
Created on Mon Mar  8 19:33:20 2021

@author: teggiba
"""

import requests
from data_in import data_in

URL = "http://127.0.0.1:5000/predict"

headers = {"Content-Type":"application/json"}
data = {"input": data_in}

r = requests.get(URL, headers=headers, json=data)


r.json()