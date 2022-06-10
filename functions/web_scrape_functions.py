#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  9 11:50:34 2022

@author: chrisgonzalez
"""
from bs4 import BeautifulSoup
import pandas as pd


def href_extract(onetable,search_param): 
    """ Input here require a onetable.find('tbody') method """
    """ search_param is a text/string """
    dat1 = onetable.find_all('td', attrs={'data-stat': search_param})
    dat2 = onetable.find_all('th', attrs={'data-stat': search_param}) 
    if len(dat1)>len(dat2):
        dat=dat1
    else:
        dat=dat2        
    # loop here to grab all hrefs    
    names=[]
    href=[]
    for j in range(len(dat)):
        try:
            names.append(dat[j].a.get_text())
            href.append(dat[j].a.get('href'))
        except:
            names.append('')
            href.append('')                        
            pass
    """ return labels and hrefs """
    return names, href


def colname_cleanup(df_temp):
    """ Input here is pandas dataframe """
    # deal with column names that have multiple headers 
    if str(type(df_temp.columns))=="<class 'pandas.core.indexes.multi.MultiIndex'>":
        col0=df_temp.columns.get_level_values(0).tolist()
        col1=df_temp.columns.get_level_values(1).tolist()
        col_final=[]
        for x,y in zip(col0,col1):
            if 'Unnamed' in x:
                x=''
            if 'Unnamed' in y:
                y=''
            if x=='':
                col_final.append(x+''+y)
            else:
                col_final.append(x+'_'+y)            
        df_temp.columns=col_final
        """ Output is same dataframe as Input,
            with cleaned column names """
    return df_temp
    






