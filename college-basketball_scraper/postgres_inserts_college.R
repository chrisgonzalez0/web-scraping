## Change working directory for local run and data set location
setwd("/Users/chrisgonzalez/Documents/web-scraping/college-basketball_scraper/")

library(DBI)
con <- dbConnect(RPostgres::Postgres(),
                 dbname = 'postgres', 
                 host = 'localhost', 
                 port = 5432,
                 user = 'postgres',
                 password = 'estarguars')

## Team Inserts 
load("r-data/cbb_teams_years.RData")
years_df$School=trimws(gsub("''","'",substr(years_df$School,2,nchar(years_df$School)-1)))
years_df$tourney=trimws(gsub("''","'",substr(years_df$tourney,2,nchar(years_df$tourney)-1)))
years_df$id=trimws(gsub("''","'",substr(years_df$id,2,nchar(years_df$id)-1)))

dbWriteTable(con, "cbb_teams", years_df, append=TRUE, row.names=FALSE)
rm(years_df)
## Inserted cbb_teams done 


# College Rosters Inserts 
load("r-data/cbb_rosters.RData")
rosters$Player=trimws(gsub("''","'",substr(rosters$Player,2,nchar(rosters$Player)-1)))
rosters$Class=trimws(gsub("''","'",substr(rosters$Class,2,nchar(rosters$Class)-1)))
rosters$Pos=trimws(gsub("''","'",substr(rosters$Pos,2,nchar(rosters$Pos)-1)))
rosters$Height=trimws(gsub("''","'",substr(rosters$Height,2,nchar(rosters$Height)-1)))
rosters$id=trimws(gsub("''","'",substr(rosters$id,2,nchar(rosters$id)-1)))
rosters$team=trimws(gsub("''","'",substr(rosters$team,2,nchar(rosters$team)-1)))

dbWriteTable(con, "cbb_rosters", rosters, append=TRUE, row.names=FALSE)
rm(rosters)
## Inserted cbb_rosters done 


# Box Scores Inserts, Loop over every file saved
files=list.files(path="r-data/")
files=files[grepl("boxscores",files)]

rowcount=0
for(j in 1:length(files)){
  print(j)
  load( paste("r-data/", files[j],sep="") )
  box=unique(box)
  dbWriteTable(con, "cbb_boxscores", box, append=TRUE, row.names=FALSE)
  print(nrow(box))
  rowcount=rowcount+nrow(box)
  rm(box)
}
print(rowcount)
## Inserted cbb_boxscores done 

## Write Schedules into db 
load("r-data/cbb_schedules.RData")  
schedules$team_id=trimws(gsub("''","'",substr(schedules$team_id,2,nchar(schedules$team_id)-1)))
dbWriteTable(con, "cbb_schedules", schedules, append=TRUE, row.names=FALSE)
rm(schedules)
## Inserted cbb_schedules done 

dbDisconnect(con)
rm(con)
gc()
