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


##### ROSTER DATA (2 Data frames for upload roster1,roster2) #####
roster_files=[x for x in files if "roster" in x]
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
## player id
split_str=[str(x).replace("/players/", "") for x in roster1['player_href'] ]
split_str = [ re.search('/(.*).htm', x) for x in split_str ]
split_str=[ x.group(1) for x in split_str ]
roster1['player_id']=split_str
## year
split_str=[str(x).replace("/teams/", "") for x in roster1['team_href'] ]
split_str = [ re.search('/(.*).htm', x) for x in split_str ]
split_str=[ x.group(1) for x in split_str ]
roster1['year']=split_str
## team id 
split_str=[str(x).replace("/teams", "") for x in roster1['team_href'] ]
split_str = [ re.search('/(.*)/', x) for x in split_str ]
split_str=[ x.group(1) for x in split_str ]
roster1['team_id']=split_str


roster2.columns=['number','player','age','pos','g','gs','wt','ht','college_univ','birthdate','yrs','av',
                 'drafted_tm_rnd_yr','salary','table_id','player_href','team_href']
## player id
split_str=[str(x).replace("/players/", "") for x in roster2['player_href'] ]
split_str = [ re.search('/(.*).htm', x) for x in split_str ]
split_str=[ x.group(1) for x in split_str ]
roster2['player_id']=split_str
## year
split_str=[str(x).replace("/teams/", "") for x in roster2['team_href'] ]
split_str = [ re.search('/(.*).htm', x) for x in split_str ]
split_str=[ x.group(1) for x in split_str ]
roster2['year']=split_str
## team id 
split_str=[str(x).replace("/teams", "") for x in roster2['team_href'] ]
split_str = [ re.search('/(.*)/', x) for x in split_str ]
split_str=[ x.group(1) for x in split_str ]
roster2['team_id']=split_str
############################################################################


###### player to college map ######
ph = pd.read_pickle('player_hrefs_df.pkl')
ph.columns=['player_href','college_href']
## player id
split_str=[str(x).replace("/players/", "") for x in ph['player_href'] ]
split_str = [ re.search('/(.*).htm', x) for x in split_str ]
split_str=[ x.group(1) for x in split_str ]
ph['player_id']=split_str
## college id
split_str=[str(x).replace("<a href=\"https://www.sports-reference.com/cfb/players", "") for x in ph['college_href'] ]
split_str = [ re.search('/(.*).htm', x) for x in split_str ]
split_str=[ x.group(1) for x in split_str if x]
ph['college_id']=''
ph['college_id'][ph['college_href']!=''] =split_str
############################################################################


###### summary of every year data ######
years_files=[x for x in files if "years" in x]
year_dfs=pd.read_pickle(years_files[0])



games_files=[x for x in files if "games" in x]



