#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 19 11:45:44 2022

@author: chrisgonzalez
"""

## general libraries
import pandas as pd
import psycopg2

## used for pandas.to_sql
## connection to target 
from sqlalchemy import create_engine

""" Commented out blocks or for transferring to AWS DB """
""" engine_target = create_engine('aws creds') """


## connect to source
source_connection = psycopg2.connect(user="postgres",
                              password="estarguars",
                                  host="localhost",
                                  port="5432",
                                  database="postgres")
source_cursor = source_connection.cursor()

## query all tables to copy in source
source_cursor.execute("SELECT table_name FROM information_schema.tables WHERE ( table_schema = 'public')ORDER BY table_schema, table_name;")
list_tables=  pd.DataFrame(source_cursor.fetchall(),columns=[desc[0] for desc in source_cursor.description])

for i in range(0,list_tables.size):
    print(i)
    source_cursor.execute("SELECT * from "+list_tables.iloc[i,0])    
    table=  pd.DataFrame(source_cursor.fetchall(),columns=[desc[0] for desc in source_cursor.description])
    try:
        table=table.drop(labels=['index'],axis=1)
    except:
        print('no drop index available')
    
    print('table name: '+list_tables.iloc[i,0])
    print('local production size: '+str(table.shape))
    print('column names: '+str(table.columns.to_list()))
    
    """ Add to dropbox code here, save as CSV and upload """
    table.to_csv('/Users/chrisgonzalez/'+list_tables.iloc[i,0]+'.csv')
    
    """ AWS code
    table.to_sql(list_tables.iloc[i,0],engine_target,if_exists='append',index=False)
    print('target table row number:')
    print(engine_target.execute('select count(*) from '+list_tables.iloc[i,0]).fetchall())
    
    print('the numerical values should match here each iteration')
    """


source_cursor.close()
source_connection.close()

""" AWS code
engine_target.dispose() """






