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
import sys

os.chdir('/Users/chrisgonzalez/web-scraping/college-football-scraping/')

# Import web scraping functions 
sys.path.insert(1, '/Users/chrisgonzalez/web-scraping/functions/')
from web_scrape_functions import colname_cleanup
from web_scrape_functions import href_extract

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
conference_teams=conference_teams.loc[ conference_teams['college_href']!='' , : ]

""" save datasets """            
with open('conference_teams.pkl', 'wb') as f:
    pickle.dump(conference_teams, f)
with open('conference_awards.pkl', 'wb') as f:
    pickle.dump(conference_awards, f)


### start college by college ###
colleges_href=conference_teams['college_href'].to_list()

# grab roster first
#'https://www.sports-reference.com/cfb/schools/georgia/2020.html'
#https://www.sports-reference.com/cfb/schools/georgia/2020-roster.html
#https://www.sports-reference.com/cfb/schools/georgia/2020-schedule.html
roster=pd.DataFrame(columns=['Player', 'Class', 'Pos', 'Summary', 'player_href', 'college_href'])
## grab roster
for k in range(len(colleges_href)):
    URL = "https://www.sports-reference.com"+colleges_href[k].replace('.html','-roster.html')  
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
    try: 
        df=pd.read_html(text)
    except:
        continue
        pass
        
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

        ## dataset for roster ##
        if onetable['id']=='roster':      
            ## for multi index header situation, table layout is different
            onetable=onetable.find('tbody')
                
            names,href=href_extract(onetable, 'player')
            df_temp['player_href']=href
            
            df_temp['college_href']=colleges_href[k]
            
            roster=pd.concat([roster,df_temp])
""" save datasets """            
with open('college_rosters.pkl', 'wb') as f:
    pickle.dump(roster, f)
            

# grab schedule next
#'https://www.sports-reference.com/cfb/schools/georgia/2020.html'
#https://www.sports-reference.com/cfb/schools/georgia/2020-schedule.html
schedule=pd.DataFrame(columns=['G','Date','Time','Day','School','home_away','Opponent','Conf',
                               'w_l','Pts','Opp','W','L','Streak','Notes','table_id','boxscore_href', 
                               'opp_href','opp_conf_href','college_href'])

## grab schedule
for k in range(len(colleges_href)):
    URL = "https://www.sports-reference.com"+colleges_href[k].replace('.html','-schedule.html')  
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

        ## dataset for schedule ##
        if onetable['id']=='schedule':      
            ## for multi index header situation, table layout is different
            onetable=onetable.find('tbody')
                
            names,href=href_extract(onetable, 'date_game')
            df_temp['boxscore_href']=href
            
            names,href=href_extract(onetable, 'opp_name')
            df_temp['opp_href']=href
            
            names,href=href_extract(onetable, 'conf_abbr')
            df_temp['opp_conf_href']=href

            df_temp['college_href']=colleges_href[k]
            
            if len(df_temp.columns)==19:
                df_temp.columns=['G','Date','Day','School','home_away','Opponent','Conf',
                                 'w_l','Pts','Opp','W','L','Streak','Notes','table_id','boxscore_href',
                                 'opp_href','opp_conf_href','college_href']
            if len(df_temp.columns)==20:
                df_temp.columns=['G','Date','Time','Day','School','home_away','Opponent','Conf',
                             'w_l','Pts','Opp','W','L','Streak','Notes','table_id','boxscore_href',
                             'opp_href','opp_conf_href','college_href']
                                    
            schedule=pd.concat([schedule,df_temp])
""" save datasets """            
with open('college_schedule.pkl', 'wb') as f:
    pickle.dump(schedule, f)

## need each player height and weight
## start with player pages first 
player_hrefs=roster['player_href'].to_list()
player_hrefs=list(set(player_hrefs))
player_hrefs=[x for x in player_hrefs if x not in '']

## build dataframe 
player_stats=pd.DataFrame(player_hrefs)
player_stats['height']=''
player_stats['weight']=''
## grab player page
for k in range(len(player_hrefs)):
    URL = "https://www.sports-reference.com"+player_hrefs[k]
    # grab main url
    r = requests.get(URL)
    text=r.content   # get request content
    
    # allow all tables to show, replace commented out code blocks
    text=text.replace(b'<!--',b'')
    text=text.replace(b'-->',b'')
    
    # parse fully viewed page
    soup = BeautifulSoup(text, 'html.parser')

    # find all table elements
    parsed_table = soup.find_all('p')
    height=''
    weight=''    
    for x in range(len(parsed_table)):
        check=parsed_table[x].find_all('span')
        if len(check)!=0:
            for j in range(len(check)):
                if height!='' and weight!='':
                    break

                if 'height' in str(check[j]).lower():
                    height=str(check[j])
                    continue
                if 'weight' in str(check[j]).lower():
                    weight=str(check[j])
                    continue
        if height!='' and weight!='':
            break
    
    player_stats['height'][k]=height
    player_stats['weight'][k]=weight
    
""" save datasets """            
with open('college_player_stats.pkl', 'wb') as f:
    pickle.dump(player_stats, f)


## need every boxscore stat
scoring_summary=pd.DataFrame(columns=['Quarter','Time','Team','Description', 
                                      'away_score','home_score','table_id','scoring_team_href',
                                      'boxscore_href'])
passing=pd.DataFrame(columns=['Player','School','Passing_Cmp','Passing_Att','Passing_Pct',
                              'Passing_Yds','Passing_Y/A','Passing_AY/A','Passing_TD',
                              'Passing_Int','Passing_Rate','player_href','college_href','boxscore_href'])


boxscore_hrefs=schedule['boxscore_href'].to_list()
boxscore_hrefs=list(set(boxscore_hrefs))
for k in range(len(boxscore_hrefs)):
    URL = "https://www.sports-reference.com"+boxscore_hrefs[k]
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
    try: 
        df=pd.read_html(text)
    except:
        continue
        pass
        
    # loop to get all hrefs and clean up tables
    for i in range(len(parsed_table)):
        # check
        onetable=parsed_table[i]
        df_temp=df[i]
        df_temp=colname_cleanup(df_temp)
        
        # retrieves table id
        try:
            #print(onetable['id'])
            df_temp['table_id']=onetable['id']  
        except: 
            continue
            pass

        ## dataset for scoring part 1 ##
        if onetable['id']=='scoring' and len(df_temp.columns)==7:      
            ## for multi index header situation, table layout is different
            onetable=onetable.find('tbody')
                
            names,href=href_extract(onetable, 'team')
            df_temp['scoring_team_href']=href
            
            df_temp['boxscore_href']=boxscore_hrefs[k]
            df_temp.columns=['Quarter','Time','Team','Description', 'away_score', 'home_score',
                             'table_id','scoring_team_href','boxscore_href']
            
            scoring_summary=pd.concat([scoring_summary,df_temp])
            
        ## dataset for passing ##
        if onetable['id']=='passing':      
            ## for multi index header situation, table layout is different
            onetable=onetable.find('tbody')
                
            names,href=href_extract(onetable, 'player')            
            df_temp=df_temp.loc[df_temp['Player']!='Player',:]
            df_temp['player_href']=href
                        
            names,href=href_extract(onetable, 'school_name')
            df_temp=df_temp.loc[~df_temp['Player'].isna(),:]
            df_temp['college_href']=href
            
            df_temp['boxscore_href']=boxscore_hrefs[k]
            passing=pd.concat([passing,df_temp])





        ## dataset for scoring part 2 ##
        if onetable['id']=='scoring' and len(df_temp.columns)==16:      
            ## for multi index header situation, table layout is different
            onetable=onetable.find('tbody')
                
            names,href=href_extract(onetable, 'date_game')
            df_temp['boxscore_href']=href




scoring - check 
passing - check 
rushing_and_receiving
defense
returns
kicking_and_punting
scoring - dont need 