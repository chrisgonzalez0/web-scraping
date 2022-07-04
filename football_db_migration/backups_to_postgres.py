#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  4 10:07:18 2022

@author: chrisgonzalez

Upload backed up dropbox files saved as CSVs to Local Database

"""
import pandas as pd
import os

## connect to local db
from sqlalchemy import create_engine
import psycopg2
engine = create_engine('postgresql://postgres:estarguars@localhost:5432/postgres')

## get files from downloaded dropbox folder
os.chdir('/Users/chrisgonzalez/Downloads/football-data/')
files=os.listdir()


## write to db
for i in range(len(files)):    
    print(files[i])
    data=pd.read_csv(files[i],index_col=0)
    data.to_sql(files[i].replace('.csv', ''),engine,if_exists='append',index=False)
    print(files[i].replace('.csv', ''))

### should be done here ###


