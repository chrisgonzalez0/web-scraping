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
conferences.to_sql('cfb_conferences', engine,if_exists='append',index=False)
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
all_awards.to_sql('cfb_awards', engine,if_exists='append',index=False)
del(all_awards,awards,conf_awards)

### conference teams data frame ###
conf_teams=pd.read_pickle('conference_teams.pkl')
conf_teams['year']=substr_pandas_col( replace_pandas_col(conf_teams['college_href'], '/cfb/schools/', ''), '/','.html')
conf_teams['college_href']=substr_pandas_col( replace_pandas_col(conf_teams['college_href'], '/cfb/schools/', ''), '','/')
conf_teams['conference_href']=substr_pandas_col( replace_pandas_col(conf_teams['conference_href'], '/cfb/conferences/', ''), '','/')
# insert to postgres
conf_teams=conf_teams.drop(labels=['Polls_AP Curr'],axis=1)
conf_teams.to_sql('cfb_conference_teams',engine,if_exists='append',index=False)
del(conf_teams)

### college rosters data frame ###
rosters=pd.read_pickle('college_rosters.pkl')
rosters['year']=substr_pandas_col( replace_pandas_col(rosters['college_href'], '/cfb/schools/', ''), '/','.html')
rosters['college_href']=substr_pandas_col( replace_pandas_col(rosters['college_href'], '/cfb/schools/', ''), '','/')
rosters['player_href']=substr_pandas_col( replace_pandas_col(rosters['player_href'], '/cfb/', ''), '/','.html')
# insert to postgres
rosters.to_sql('cfb_rosters',engine,if_exists='append',index=False)
del(rosters)

### college player stats ###
keys=engine.execute('select distinct player_href from cfb_player_ht_wt')
keys=[x[0] for x in keys]

player_stats=pd.read_pickle('college_player_stats.pkl')
player_stats.columns=['player_href','height','weight']
player_stats['player_href']=substr_pandas_col( replace_pandas_col(player_stats['player_href'], '/cfb/', ''), '/','.html')
player_stats['height']=substr_pandas_col(player_stats['height'],'<span itemprop="height">' , '</span>')
player_stats['weight']=substr_pandas_col(player_stats['weight'],'<span itemprop="weight">' , 'lb</span>')

player_stats=player_stats[~player_stats.player_href.isin(keys)]
# insert to postgres
player_stats.to_sql('cfb_player_ht_wt',engine,if_exists='append',index=False)
del(player_stats,keys)

### college schedules ###
schedule=pd.read_pickle('college_schedule.pkl')
schedule['year']=substr_pandas_col( replace_pandas_col(schedule['college_href'], '/cfb/schools/', ''), '/','.html')
schedule['college_href']=substr_pandas_col( replace_pandas_col(schedule['college_href'], '/cfb/schools/', ''), '','/')
schedule['opp_href']=substr_pandas_col( replace_pandas_col(schedule['opp_href'], '/cfb/schools/', ''), '','/')
schedule['boxscore_href']=substr_pandas_col(schedule['boxscore_href'], '/cfb/boxscores/', '.html')
schedule['opp_conf_href']=substr_pandas_col( replace_pandas_col(schedule['opp_conf_href'], '/cfb/conferences/', ''), '','/')
# insert to postgres
schedule.to_sql('cfb_schedule',engine,if_exists='append',index=False)
del(schedule)

### college scoring plays ###
scoring=pd.read_pickle('college_scoring.pkl')
scoring['year']=substr_pandas_col( replace_pandas_col(scoring['scoring_team_href'], '/cfb/schools/', ''), '/','.html')
scoring['scoring_team_href']=substr_pandas_col( replace_pandas_col(scoring['scoring_team_href'], '/cfb/schools/', ''), '','/')
scoring['boxscore_href']=substr_pandas_col(scoring['boxscore_href'], '/cfb/boxscores/', '.html')
# insert to postgres
scoring.to_sql('cfb_scoring_plays',engine,if_exists='append',index=False)
del(scoring)

### college passing plays ###
passing=pd.read_pickle('college_passing.pkl')
passing['year']=substr_pandas_col( replace_pandas_col(passing['college_href'], '/cfb/schools/', ''), '/','.html')
passing['college_href']=substr_pandas_col( replace_pandas_col(passing['college_href'], '/cfb/schools/', ''), '','/')
passing['boxscore_href']=substr_pandas_col(passing['boxscore_href'], '/cfb/boxscores/', '.html')
passing['player_href']=substr_pandas_col( replace_pandas_col(passing['player_href'], '/cfb/', ''), '/','.html')
# insert to postgres
passing.to_sql('cfb_passing',engine,if_exists='append',index=False)
del(passing)

### college rush/receiving plays ###
rush_rec=pd.read_pickle('college_rush_rec.pkl')
rush_rec['year']=substr_pandas_col( replace_pandas_col(rush_rec['college_href'], '/cfb/schools/', ''), '/','.html')
rush_rec['college_href']=substr_pandas_col( replace_pandas_col(rush_rec['college_href'], '/cfb/schools/', ''), '','/')
rush_rec['boxscore_href']=substr_pandas_col(rush_rec['boxscore_href'], '/cfb/boxscores/', '.html')
rush_rec['player_href']=substr_pandas_col( replace_pandas_col(rush_rec['player_href'], '/cfb/', ''), '/','.html')
# insert to postgres
rush_rec.to_sql('cfb_rush_rec',engine,if_exists='append',index=False)
del(rush_rec)

### college defense ###
defense=pd.read_pickle('college_defense.pkl')
defense['year']=substr_pandas_col( replace_pandas_col(defense['college_href'], '/cfb/schools/', ''), '/','.html')
defense['college_href']=substr_pandas_col( replace_pandas_col(defense['college_href'], '/cfb/schools/', ''), '','/')
defense['boxscore_href']=substr_pandas_col(defense['boxscore_href'], '/cfb/boxscores/', '.html')
defense['player_href']=substr_pandas_col( replace_pandas_col(defense['player_href'], '/cfb/', ''), '/','.html')
# insert to postgres
defense.to_sql('cfb_defense',engine,if_exists='append',index=False)
del(defense)

### college kick returns ###
kick_returns=pd.read_pickle('college_returns.pkl')
kick_returns['year']=substr_pandas_col( replace_pandas_col(kick_returns['college_href'], '/cfb/schools/', ''), '/','.html')
kick_returns['college_href']=substr_pandas_col( replace_pandas_col(kick_returns['college_href'], '/cfb/schools/', ''), '','/')
kick_returns['boxscore_href']=substr_pandas_col(kick_returns['boxscore_href'], '/cfb/boxscores/', '.html')
kick_returns['player_href']=substr_pandas_col( replace_pandas_col(kick_returns['player_href'], '/cfb/', ''), '/','.html')
# insert to postgres
kick_returns.to_sql('cfb_kick_returns',engine,if_exists='append',index=False)
del(kick_returns)

### college kicking ###
kicking=pd.read_pickle('college_kick.pkl')
kicking['year']=substr_pandas_col( replace_pandas_col(kicking['college_href'], '/cfb/schools/', ''), '/','.html')
kicking['college_href']=substr_pandas_col( replace_pandas_col(kicking['college_href'], '/cfb/schools/', ''), '','/')
kicking['boxscore_href']=substr_pandas_col(kicking['boxscore_href'], '/cfb/boxscores/', '.html')
kicking['player_href']=substr_pandas_col( replace_pandas_col(kicking['player_href'], '/cfb/', ''), '/','.html')
# insert to postgres
kicking.to_sql('cfb_kicking',engine,if_exists='append',index=False)
del(kicking)









