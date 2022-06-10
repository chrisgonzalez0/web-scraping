#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 10 10:52:20 2022

@author: chrisgonzalez
"""
## libraries
import pandas as pd
import os
import pickle
import re

## local postgres connections
from sqlalchemy import create_engine
import psycopg2
engine = create_engine('postgresql://postgres:estarguars@localhost:5432/postgres')

os.chdir('/Users/chrisgonzalez/web-scraping/college-football-scraping/')
files=os.listdir()

## functions for data cleaning 
def replace_pandas_col(col,pattern,replacement):
    """ col is a pandas column """
    repl=[str(x).replace(pattern, replacement) for x in col ]
    return repl

def substr_pandas_col(col,start,end):
    """ col is a pandas column """
    split_str = [ re.search(start+'(.*)'+end, x) for x in col ]
    split_str = [ x.group(1) if x is not None else '' for x in split_str ]
    return split_str


### start with conferences data frame ### 
conferences=pd.read_pickle('conferences.pkl')
conferences['conference_href']=substr_pandas_col( replace_pandas_col(conferences['conference_href'], '/cfb/conferences/', ''), '','/')
conferences['conf_champ_href']=substr_pandas_col( replace_pandas_col(conferences['conf_champ_href'], '/cfb/schools/', ''), '','/')
# insert to postgres
conferences.to_sql('cfb_conferences', engine)
del(conferences)

### awards data frame ###
awards=pd.read_pickle('all_awards.pkl')
conf_awards=pd.read_pickle('conference_awards.pkl')
conf_awards['year']=substr_pandas_col( replace_pandas_col(conf_awards['college_href'], '/cfb/schools/', ''), '/','.html')

awards['conference_href']='all'
conf_awards['conference_href']=substr_pandas_col( replace_pandas_col(conf_awards['conference_href'], '/cfb/conferences/', ''), '','/')

awards['award_name_href']=substr_pandas_col(awards['award_name_href'], '/cfb/awards/','.html')
conf_awards['award_name_href']=substr_pandas_col(conf_awards['award_name_href'], '/cfb/awards/','.html')

awards['player_href']=substr_pandas_col( replace_pandas_col(awards['player_href'], '/cfb/', ''), '/','.html')
conf_awards['player_href']=substr_pandas_col( replace_pandas_col(conf_awards['player_href'], '/cfb/', ''), '/','.html')

awards['college_href']=substr_pandas_col( replace_pandas_col(awards['college_href'], '/cfb/schools/', ''), '','/')
conf_awards['college_href']=substr_pandas_col( replace_pandas_col(conf_awards['college_href'], '/cfb/schools/', ''), '','/')
# insert to postgres
all_awards=pd.concat([awards,conf_awards])
all_awards.to_sql('cfb_awards', engine)
del(all_awards,awards,conf_awards)

### conference teams data frame ###
conf_teams=pd.read_pickle('conference_teams.pkl')
conf_teams['year']=substr_pandas_col( replace_pandas_col(conf_teams['college_href'], '/cfb/schools/', ''), '/','.html')
conf_teams['college_href']=substr_pandas_col( replace_pandas_col(conf_teams['college_href'], '/cfb/schools/', ''), '','/')
conf_teams['conference_href']=substr_pandas_col( replace_pandas_col(conf_teams['conference_href'], '/cfb/conferences/', ''), '','/')
# insert to postgres
conf_teams.to_sql('cfb_conference_teams',engine)
del(conf_teams)

