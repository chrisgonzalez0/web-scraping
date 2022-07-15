setwd("/Users/chrisgonzalez/Documents/web-scraping/nba-scraping/")

library(DBI)
con <- dbConnect(RPostgres::Postgres(),
                 dbname = 'postgres', 
                 host = 'localhost', 
                 port = 5432,
                 user = 'postgres',
                 password = 'estarguars')

## add player key to db
load("r-data/nba_player_key.RData")
dbWriteTable(con, "bb_player_keys", player_key, append=TRUE, row.names=FALSE)
rm(player_key)
## Inserted Player Keys done 


# NBA Seasons Inserted Here  
load("r-data/nba_teams.RData")
dbWriteTable(con, "nba_teams", final_data, append=TRUE, row.names=FALSE)
rm(final_data)
## Inserted nba_teams done 

## Schedules Insert Here 
load("r-data/nba_schedules.RData")
colnames(temp)=c("g","date","time","network","box_score","home_away","opponent","outcome","game_length","team_score","opp_score","wins","losses","streak","notes","team_id","year","game_type","box_score_id","opp_team_id")
dbWriteTable(con, "nba_schedules", temp, append=TRUE, row.names=FALSE)
rm(temp)
## Inserted nba_schedules done 


## Rosters Then All box scores left
load("r-data/nba_roster.RData")
dbWriteTable(con, "nba_rosters", roster, append=TRUE, row.names=FALSE)
rm(roster)
## Inserted nba_rosters done 

## Box Scores Upload 
boxscore_files=list.files("r-data/")
boxscore_files=boxscore_files[grepl("box",boxscore_files)]

for(j in 1:length(boxscore_files)){
  load( paste("r-data/",boxscore_files[j],sep="") )
  boxscores=unique(boxscores)
  dbWriteTable(con, "nba_boxscores", boxscores, append=TRUE, row.names=FALSE)
  print(nrow(boxscores))
  rm(boxscores)
}
## Inserted nba_boxscores done     
  
