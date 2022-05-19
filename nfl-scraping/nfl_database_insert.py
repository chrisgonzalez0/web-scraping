#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 30 14:03:33 2022

@author: chrisgonzalez
"""


import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import pickle
import re

os.chdir('/Users/chrisgonzalez/web-scraping/nfl-scraping/')

