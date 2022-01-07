#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan  3 13:33:49 2022

@author: chrisgonzalez
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import pickle

os.chdir('/Users/chrisgonzalez/web-scraping/nfl-scraping/')



#### years loop ####
years=[2020,2019,2018,2017,2016,2015,2014,2013,2012,2011,2010,2009,2008,2007,2006,2005]

team_refs=[]
for yearsi in years:
    
    URL = "https://www.pro-football-reference.com/years/"+str(yearsi)+"/"    
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
    
    years_tables=[]
    
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
        df_temp['table_id']=onetable['id']  
        
        # skip playoff data set
        if onetable['id']=='playoff_results':
            continue
            
        # remove asterisk points
        df_temp['Tm']=df_temp['Tm'].replace({"\+":""},regex=True)
        df_temp['Tm']=df_temp['Tm'].replace({"\*":""},regex=True)
        
        ## for multi index header situation, table layout is different
        onetable=onetable.find('tbody')
        
        # table structure logic
        dat1 = onetable.find_all('td', attrs={'data-stat': 'team'})
        dat2 = onetable.find_all('th', attrs={'data-stat': 'team'}) 
        if len(dat1)>len(dat2):
            dat=dat1
        else:
            dat=dat2
        
        
        """
        if multiindex_flag==1:
            dat = onetable.find_all('td', attrs={'data-stat': 'team'}) 
        else:
            dat = onetable.find_all('th', attrs={'data-stat': 'team'}) # get all team references
        """
        
        # loop here to grab all href and filter rows to teams    
        team_names=[]
        href=[]
        for j in range(len(dat)):
            try:
                team_names.append(dat[j].a.get_text())
                href.append(dat[j].a.get('href'))
            except:
                pass
        team_names=[sub.replace("\+","") for sub in team_names]
        team_names=[sub.replace("\*","") for sub in team_names]
        
        # filter pandas df to team names and add columns
        df_temp=df_temp.loc[df_temp['Tm'].isin(team_names),:]
        df_temp['href']=href
        df_temp['year']=yearsi
        team_refs.append(href)
        
        years_tables.append(df_temp)
        
        # save years data into python list
        with open('years_'+str(yearsi)+'.pkl', 'wb') as f:
            pickle.dump(years_tables, f)
#### end loop for years data ####

        
    
## need to grab schedules and box scores href, team rosters player href, box score data and advanced stats (if any)
# unique team references
team_refs=[item for sublist in team_refs for item in sublist]
team_refs=list(set(team_refs))

box_score_refs=[]    
for tr in range(len(team_refs)):
    sched_url="https://www.pro-football-reference.com/"+team_refs[tr]
    # grab main url
    r = requests.get(sched_url)
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
        
    # box score href
    for i in range(len(parsed_table)):
        # check
        onetable=parsed_table[i]
            
        if onetable['id']!='games':
            continue
            
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
        df_temp['table_id']=onetable['id']
                        
        ## for multi index header situation, table layout is different
        onetable=onetable.find('tbody')
        # table structure logic
        dat1 = onetable.find_all('td', attrs={'data-stat': 'boxscore_word'})
        dat2 = onetable.find_all('th', attrs={'data-stat': 'boxscore_word'}) 
        if len(dat1)>len(dat2):
            dat=dat1
        else:
            dat=dat2
        # loop here to grab all boxscore href   
        boxscore_href=[]
        for j in range(len(dat)):
            try:
                boxscore_href.append(dat[j].a.get('href'))
            except:
                pass
        df_temp=df_temp.loc[df_temp['Opp']!='Bye Week',:]
        df_temp=df_temp.loc[df_temp['Opp'].notna(),:]
        
        df_temp['boxscore_id']=boxscore_href
        df_temp['team_href']=team_refs[tr]
    box_score_refs.append(boxscore_href)
    print(team_refs[tr])
    print(df_temp.shape)
    
    file_label=team_refs[tr].replace('/teams/','')
    file_label=file_label.replace('.htm','')
    file_label=file_label.replace('/','_')
    file_label=file_label+'_games'
    with open(file_label+'.pkl', 'wb') as f:
        pickle.dump(df_temp, f)
#### schedule loop ends here ####


## team rosters loop
player_hrefs=[]
for tr in range(len(team_refs)):
    roster_url="https://www.pro-football-reference.com/"+team_refs[tr].replace('.htm','_roster.htm')
    # grab main url
    r = requests.get(roster_url)
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
    
    # player href
    roster_tables=[]
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
        df_temp['table_id']=onetable['id']
                        
        ## for multi index header situation, table layout is different
        onetable=onetable.find('tbody')
        # table structure logic
        dat1 = onetable.find_all('td', attrs={'data-stat': 'player'})
        dat2 = onetable.find_all('th', attrs={'data-stat': 'player'}) 
        if len(dat1)>len(dat2):
            dat=dat1
        else:
            dat=dat2
        # loop here to grab all boxscore href
        player_name=[]
        player_href=[]
        for j in range(len(dat)):
            try:
                player_name.append(dat[j].a.get_text())                
                player_href.append(dat[j].a.get('href'))
            except:
                pass
        
        # remove asterisk points
        player_name=[sub.replace("\+","") for sub in player_name]
        player_name=[sub.replace("\*","") for sub in player_name]
        player_name=[sub.strip() for sub in player_name]

        df_temp['Player']=df_temp['Player'].replace({"\+":""},regex=True)
        df_temp['Player']=df_temp['Player'].replace({"\*":""},regex=True)
        df_temp['Player']=df_temp['Player'].str.strip()
    
        # filter pandas df to player names and add columns
        df_temp=df_temp.loc[df_temp['Player'].isin(player_name),:]
        df_temp['player_href']=player_href
        df_temp['team_href']=team_refs[tr]  
        print(df_temp.shape)
        
        player_hrefs.append(player_href)   ## to get college_id
        roster_tables.append(df_temp)      ## save tables into list of tables
                
    print(team_refs[tr])
    
    file_label=team_refs[tr].replace('/teams/','')
    file_label=file_label.replace('.htm','')
    file_label=file_label.replace('/','_')
    file_label=file_label+'_roster'
    with open(file_label+'.pkl', 'wb') as f:
        pickle.dump(roster_tables, f)






box_score_refs=[item for sublist in box_score_refs for item in sublist]
box_score_refs=list(set(box_score_refs))
          
        

        
        
        
        
        
    
    ## year loop done ##
    print(years[yy])





# header
tname=onetable.find_all('data-stat')
tname=tname.find('data-stat')

row=t.find_all('thead')

rr=row.find('th', attrs={'data-stat'})



df = []