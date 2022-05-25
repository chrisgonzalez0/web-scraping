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

years=pd.DataFrame(columns=['Tm','W','L','W-L%','PF','PA','PD','MoV',
                            'SoS','SRS','OSRS','DSRS','table_id','href','year'])

for i in range(len(years_files)):
    years_dfs=pd.read_pickle(years_files[i])
    years=pd.concat([years,years_dfs[0]])
    years=pd.concat([years,years_dfs[1]])

## team id 
split_str=[str(x).replace("/teams", "") for x in years['href'] ]
split_str = [ re.search('/(.*)/', x) for x in split_str ]
split_str=[ x.group(1) for x in split_str ]
years['team_id']=split_str
############################################################################
    

###### schedule data ######
games_files=[x for x in files if "games" in x]
#games_dfs=pd.read_pickle(games_files[0])
schedule=pd.DataFrame(columns=['Week','Day','Date','time','label','outcome','OT','Rec','home_away','Opp','Score_Tm','Score_Opp','Offense_1stD','Offense_TotYd',
 'Offense_PassY','Offense_RushY','Offense_TO','Defense_1stD','Defense_TotYd','Defense_PassY','Defense_RushY',
 'Defense_TO','Expected Points_Offense','Expected Points_Defense','Expected Points_Sp. Tms',
 'table_id','boxscore_href','team_href'])

for i in range(len(games_files)):
    games=pd.read_pickle(games_files[i])
    games.columns=['Week','Day','Date','time','label','outcome','OT','Rec','home_away','Opp','Score_Tm','Score_Opp','Offense_1stD','Offense_TotYd',
                   'Offense_PassY','Offense_RushY','Offense_TO','Defense_1stD','Defense_TotYd','Defense_PassY','Defense_RushY',
                   'Defense_TO','Expected Points_Offense','Expected Points_Defense','Expected Points_Sp. Tms','table_id','boxscore_href','team_href']
    schedule=pd.concat([schedule,games])
## team id 
split_str=[str(x).replace("/teams", "") for x in schedule['team_href'] ]
split_str = [ re.search('/(.*)/', x) for x in split_str ]
split_str=[ x.group(1) for x in split_str ]
schedule['team_id']=split_str
## year
split_str=[str(x).replace("/teams/", "") for x in schedule['team_href'] ]
split_str = [ re.search('/(.*).htm', x) for x in split_str ]
split_str=[ x.group(1) for x in split_str ]
schedule['year']=split_str
## boxscore_id
split_str=[str(x).replace("/boxscores", "") for x in schedule['boxscore_href'] ]
split_str = [ re.search('/(.*).htm', x) for x in split_str ]
split_str=[ x.group(1) for x in split_str ]
schedule['boxscore_id']=split_str
############################################################################


###### boxscore data ######
## offense, defemse, kick return, kicks, starters, snapcount, play by play ##
files=os.listdir('boxscores')
offense=pd.DataFrame(columns=['Player','Tm','Passing_Cmp','Passing_Att','Passing_Yds',
                              'Passing_TD','Passing_Int','Passing_Sk','Passing_Yds.1',
                              'Passing_Lng','Passing_Rate','Rushing_Att','Rushing_Yds',
                              'Rushing_TD','Rushing_Lng','Receiving_Tgt','Receiving_Rec',
                              'Receiving_Yds','Receiving_TD','Receiving_Lng','Fumbles_Fmb',
                              'Fumbles_FL','table_id','player_href','box_score_id'])
defense=pd.DataFrame(columns=['Player','Tm','Def Interceptions_Int','Def Interceptions_Yds',
                              'Def Interceptions_TD','Def Interceptions_Lng','Def Interceptions_PD',
                              'Sk','Tackles_Comb','Tackles_Solo','Tackles_Ast','Tackles_TFL',
                              'Tackles_QBHits','Fumbles_FR','Fumbles_Yds','Fumbles_TD',
                              'Fumbles_FF','table_id','player_href','box_score_id'])
kick_return=pd.DataFrame(columns=['Player','Tm','Kick Returns_Rt','Kick Returns_Yds',
                                  'Kick Returns_Y/Rt','Kick Returns_TD','Kick Returns_Lng',
                                  'Punt Returns_Ret','Punt Returns_Yds','Punt Returns_Y/R',
                                  'Punt Returns_TD','Punt Returns_Lng','table_id','player_href','box_score_id'])
kicking=pd.DataFrame(columns=['Player','Tm','Scoring_XPM','Scoring_XPA','Scoring_FGM',
                              'Scoring_FGA','Punting_Pnt','Punting_Yds','Punting_Y/P',
                              'Punting_Lng','table_id','player_href','box_score_id'])
starters=pd.DataFrame(columns=['Player','Pos','table_id','player_href','box_score_id'])
snapcount=pd.DataFrame(columns=['Player','Pos','Off._Num','Off._Pct','Def._Num','Def._Pct',
                                'ST_Num','ST_Pct','table_id','player_href','box_score_id'])
pbp=pd.DataFrame(columns=['Quarter','Time','Down','ToGo','Location','Detail','away_team','home_team',
                          'EPB','EPA','table_id','box_score_id'])


for i in range(len(files)):
    print(files[i])
    box=pd.read_pickle('boxscores/'+files[i])
    
    for j in range(len(box)):
        
        if 'player_offense'==box[j]['table_id'].unique()[0]:
            offense=pd.concat([offense,box[j]])

        if 'player_defense'==box[j]['table_id'].unique()[0]:
            defense=pd.concat([defense,box[j]])

        if 'returns'==box[j]['table_id'].unique()[0]:
            kick_return=pd.concat([kick_return,box[j]])

        if 'kicking'==box[j]['table_id'].unique()[0]:
            kicking=pd.concat([kicking,box[j]])

        if 'starters' in box[j]['table_id'].unique()[0]:
            starters=pd.concat([starters,box[j]])

        if 'snap_counts' in box[j]['table_id'].unique()[0]:
            snapcount=pd.concat([snapcount,box[j]])

        if 'pbp'==box[j]['table_id'].unique()[0]:
            box[j].columns=['Quarter','Time','Down','ToGo','Location','Detail','away_team','home_team',
                          'EPB','EPA','table_id','box_score_id']
            pbp=pd.concat([pbp,box[j]])
############################################################################


## clean data sets and formats
offense['Passing_Cmp']=offense['Passing_Cmp'].astype(float)
offense['Passing_Att']=offense['Passing_Att'].astype(float)
offense['Passing_Yds']=offense['Passing_Yds'].astype(float)

## insert to postgres
from sqlalchemy import create_engine
import psycopg2
engine = create_engine('postgresql://postgres:estarguars@localhost:5432/postgres')

## roster 1
roster1.to_sql('team_starters', engine)
## roster 2
roster2.to_sql('team_rosters',engine)
## player key 
ph.to_sql('player_keys',engine)
## year_summaries
years.to_sql('year_summaries',engine)
## team schedules
schedule.to_sql('team_schedules',engine)
## team boxscores
offense.to_sql('boxscore_offense',engine)
defense.to_sql('boxscore_defense',engine)
kick_return.to_sql('boxscore_kick_returns',engine)
kicking.to_sql('boxscore_kicking',engine)

## team stats
starters.to_sql('boxscore_starters',engine)
snapcount.to_sql('boxscore_snapcount',engine)

## play by play 
pbp['Quarter']=pbp['Quarter'].astype('string')
pbp=pbp.loc[ pbp['Quarter']!='1st Quarter'  , : ] 
pbp=pbp.loc[ pbp['Quarter']!='2nd Quarter'  , : ] 
pbp=pbp.loc[ pbp['Quarter']!='3rd Quarter'  , : ] 
pbp=pbp.loc[ pbp['Quarter']!='4th Quarter'  , : ] 
pbp=pbp.loc[ pbp['Quarter']!='Quarter'  , : ] 
pbp=pbp.loc[ pbp['Quarter']!='End of Regulation'  , : ] 
pbp=pbp.loc[ pbp['Quarter']!='End of Overtime'  , : ] 
pbp=pbp.loc[ pbp['Quarter']!='OT'  , : ] 
pbp=pbp.loc[ pbp['Quarter']!='Overtime'  , : ] 
pbp.to_sql('boxscore_pbp',engine)





