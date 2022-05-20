#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 30 14:03:33 2022

@author: chrisgonzalez
"""


import pandas as pd
import os
import pickle
import re

os.chdir('/Users/chrisgonzalez/web-scraping/nfl-scraping/')

files=os.listdir()

roster_files=[x for x in files if "roster" in x]
games_files=[x for x in files if "games" in x]
years_files=[x for x in files if "years" in x]

ph = pd.read_pickle('player_hrefs_df.pkl')

## load sample roster files and create empty master data frames
roster_dfs=pd.read_pickle(roster_files[0])
roster1_temp=roster_dfs[0]
roster2_temp=roster_dfs[1]

roster1=pd.DataFrame(columns=roster1_temp.columns)
roster2=pd.DataFrame(columns=roster2_temp.columns)

for i in range(len(roster_files)):
    roster_dfs=pd.read_pickle(roster_files[i])
    roster1_temp=roster_dfs[0]
    roster2_temp=roster_dfs[1]
    
    roster1=pd.concat([roster1,roster1_temp])
    roster2=pd.concat([roster2,roster2_temp])

del(roster1_temp,roster2_temp,roster_dfs)  
  
roster1.columns=['pos','player','age','yrs','gs','summary_of_player_stats','drafted_tm_rnd_yr','table_id','player_href','team_href']
roster2.columns=['number','player','age','pos','g','gs','wt','ht','college_univ','birthdate','yrs','av',
                 'drafted_tm_rnd_yr','salary','table_id','player_href','team_href']

