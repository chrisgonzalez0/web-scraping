#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 25 12:10:40 2022

@author: chrisgonzalez
"""
import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import pickle
import re

os.chdir('/Users/chrisgonzalez/web-scraping/college-football-scraping/')

#### years loop to get conferences and main award winners ####
years=[2020,2019,2018,2017,2016,2015,2014,2013,2012,2011,2010,2009,
       2008,2007,2006,2005,2004,2003,2002,2001]


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
    return names, href



conferences=pd.DataFrame(columns=['Rk','Conference','Schs','Overall_G','Overall_W','Overall_L',
                                  'Overall_Pct','Bowls_G','Bowls_W','Bowls_L','Bowls_Pct','SRS_SRS',
                                  'SRS_SOS','Polls_Pre','Polls_Final','Champion','table_id',
                                  'conference_href','conf_champ_href','year'])
all_awards=pd.DataFrame(columns=['Award', 'Name','School','table_id','award_name_href', 
                                 'player_href','college_href','year'])

for yearsi in years:
    
    URL = "https://www.sports-reference.com/cfb/years/"+str(yearsi)+".html"    
    # grab main url
    r = requests.get(URL)
    text=r.content   # get request content
    
    # allow all tables to show, replace commented out code blocks
    text=text.replace(b'<!--',b'')
    text=text.replace(b'-->',b'')
    
    # parse fully viewed page
    soup = BeautifulSoup(text, 'html.parser')
    
    # find all table elements
    parsed_table = soup.find_all('table')
    # find all tables
    df=pd.read_html(text)
        
    # loop to get all hrefs and clean up tables
    for i in range(len(parsed_table)):
        # check
        onetable=parsed_table[i]
        df_temp=df[i]
        
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
        
        # retrieves table id
        try:
            df_temp['table_id']=onetable['id']  
        except: 
            continue
            pass
                
        
        # only grab these table ids for datasets
        if onetable['id'] in ['conferences','all_awards']:
            
            ## dataset for conferences ##
            if onetable['id']=='conferences':                
                ## for multi index header situation, table layout is different
                onetable=onetable.find('tbody')
                
                names,href=href_extract(onetable, 'conf_name')
                df_temp['conference_href']=href

                names,href=href_extract(onetable, 'conf_champ')
                df_temp['conf_champ_href']=href
                
                
                df_temp['year']=yearsi
                conferences=pd.concat([conferences,df_temp])
                continue

            ## dataset for awards ##
            if onetable['id']=='all_awards':    
                ## for multi index header situation, table layout is different
                onetable=onetable.find('tbody')

                names,href=href_extract(onetable, 'award_name')
                df_temp['award_name_href']=href
                
                names,href=href_extract(onetable, 'name_full')
                df_temp['player_href']=href
                
                names,href=href_extract(onetable, 'school_name')
                df_temp['college_href']=href
                                
                df_temp['year']=yearsi
                all_awards=pd.concat([all_awards,df_temp])
                continue
                
## save all_awards data set and conferences data set
with open('all_awards.pkl', 'wb') as f:
    pickle.dump(all_awards, f)
with open('conferences.pkl', 'wb') as f:
    pickle.dump(conferences, f)


### conference page scraping ### 
conf_hrefs=conferences['conference_href'].to_list()

conference_teams=pd.DataFrame(columns=['Team','Overall_W','Overall_L','Overall_Pct','Conference_W',
                                       'Conference_L','Conference_Pct','Points Per Game_Off',
                                       'Points Per Game_Def','SRS_SRS','SRS_SOS','Polls_AP Pre',
                                       'Polls_AP High','Polls_AP Rank','Notes','college_href'])
conference_awards=pd.DataFrame(columns=['Award','Name','School','table_id','award_name_href',
                                        'player_href','college_href','conference_href'])
for k in range(len(conf_hrefs)):
    URL = "https://www.sports-reference.com"+conf_hrefs[k]  
    # grab main url
    r = requests.get(URL)
    text=r.content   # get request content
    
    # allow all tables to show, replace commented out code blocks
    text=text.replace(b'<!--',b'')
    text=text.replace(b'-->',b'')
    
    # parse fully viewed page
    soup = BeautifulSoup(text, 'html.parser')
    
    # find all table elements
    parsed_table = soup.find_all('table')
    # find all tables
    df=pd.read_html(text)
        
    # loop to get all hrefs and clean up tables
    for i in range(len(parsed_table)):
        # check
        onetable=parsed_table[i]
        df_temp=df[i]
        
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
            
        # retrieves table id
        try:
            df_temp['table_id']=onetable['id']  
        except: 
            continue
            pass

        # only grab these table ids for datasets
        if onetable['id'] in ['standings','all_awards']:
            
            ## dataset for standings ##
            if onetable['id']=='standings':        
                cols=df_temp.columns.to_list()
                cols[0]='Team'
                df_temp.columns=cols
                ## for multi index header situation, table layout is different
                onetable=onetable.find('tbody')
                
                names,href=href_extract(onetable,'school_name')
                df_temp['college_href']=href
                
                df_temp['conference_href']=conf_hrefs[k] 
                                
                conference_teams=pd.concat([conference_teams,df_temp])
                continue

            ## dataset for standings ##
            if onetable['id']=='all_awards':      
                ## for multi index header situation, table layout is different
                onetable=onetable.find('tbody')
                
                names,href=href_extract(onetable, 'award_name')
                df_temp['award_name_href']=href
                
                names,href=href_extract(onetable, 'name_full')
                df_temp['player_href']=href
                
                names,href=href_extract(onetable, 'school_name')
                df_temp['college_href']=href
                
                df_temp['conference_href']=conf_hrefs[k] 
                                
                conference_awards=pd.concat([conference_awards,df_temp])
                continue

## remove weird rows from conference teams
""" save datasets """            
with open('conference_teams.pkl', 'wb') as f:
    pickle.dump(conference_teams, f)
with open('conference_awards.pkl', 'wb') as f:
    pickle.dump(conference_awards, f)

