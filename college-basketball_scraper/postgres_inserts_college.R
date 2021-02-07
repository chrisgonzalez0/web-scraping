# Connect to DB
library(RPostgreSQL)
drv <- dbDriver("PostgreSQL")
con <- dbConnect(drv, dbname="basketball",user="postgres",password="estarguars",host = "localhost", port = 5432)

## Change working directory for local run and data set location
setwd("/Users/chrisgonzalez/web-scraping/college_basketball_scraper/r-data/")
load("2019_teams.RData")

## Team Inserts 
temp=teams
colnames(temp)=make.names(colnames(temp))
cols=colnames(temp)[!(make.names(colnames(temp)) %in% c("X.","X..1","X..2","X..4"))]
temp$X..3="NULL"

temp=temp[,cols]

x=paste(temp,collapse = ",",sep="")
x=apply(temp,1,function(x) { paste(x,collapse=",")})
x=paste("(",x,")",sep="")

bands <- round(seq(0,nrow(temp),length.out=(ceiling(nrow(temp)/1000)+1)))

for (i in 1:(length(bands)-1)){
  y=x[(bands[i]+1):bands[i+1]]
  y=paste(y,collapse=",",sep="")
  text=paste("insert into college_seasons (rk,school,games,wins,losses,w_l_perc,srs,sos,conf_wins,conf_losses,home_wins,home_losses,away_wins,away_losses,tm_pts,opp_pts,mp,fg,fga,fg_perc,x3p,x3pa,x3p_perc,ft,fta,ft_perc,orb,trb,ast,stl,blk,tov,pf,tourney,team_id,year) values ",y,sep="")
  check=dbGetQuery(con,text)
  print(check)
}

# College Rosters Inserts 
load("2019_rosters.RData")
rosters=rosters[,c(-2,-6,-7,-8)]
temp=rosters

x=paste(temp,collapse = ",",sep="")
x=apply(temp,1,function(x) { paste(x,collapse=",")})
x=paste("(",x,")",sep="")

bands <- round(seq(0,nrow(temp),length.out=(ceiling(nrow(temp)/1000)+1)))
for (i in 1:(length(bands)-1)){
  y=x[(bands[i]+1):bands[i+1]]
  y=paste(y,collapse=",",sep="")
  text=paste("insert into college_rosters (player,class,pos,ht,summary,player_id,team_id,year) values ",y,sep="")
  check=dbGetQuery(con,text)
  print(check)
}


# Box Scores Inserts, Loop over every file saved
files=list.files(path=".")
files=files[grepl("_pt",files)]

for(j in 1:length(files)){
  load(files[j])
  box=box[box$Starters!="Reserves",]
  box$Starters=gsub("'","''",box$Starters)
  box$Starters=paste("'",box$Starters,"'",sep="")
  box$FG=as.character(box$FG)
  box$FG[is.na(box$FG)]="0"
  box$FG[box$FG==""]="0"
  box$FGA=as.character(box$FGA)
  box$FGA[is.na(box$FGA)]="0"
  box$FGA[box$FGA==""]="0"  
  box$`FG%`=as.character(box$`FG%`)
  box$`FG%`[is.na(box$`FG%`)]="0"
  box$`FG%`[box$`FG%`==""]="0"
  box$`2P`=as.character(box$`2P`)
  box$`2P`[box$`2P`==""]="0"
  box$`2PA`=as.character(box$`2PA`)
  box$`2PA`[box$`2PA`==""]="0"
  box$`2P%`=as.character(box$`2P%`)
  box$`2P%`[box$`2P%`==""]="0"

  box$`3P`=as.character(box$`3P`)
  box$`3P`[box$`3P`==""]="0"
  box$`3PA`=as.character(box$`3PA`)
  box$`3PA`[box$`3PA`==""]="0"
  box$`3P%`=as.character(box$`3P%`)
  box$`3P%`[box$`3P%`==""]="0"

  box$FT=as.character(box$FT)
  box$FT[box$FT==""]="0"
  box$FTA=as.character(box$FTA)
  box$FTA[box$FTA==""]="0"
  box$`FT%`=as.character(box$`FT%`)
  box$`FT%`[box$`FT%`==""]="0"

  box$MP=as.character(box$MP)
  box$MP[box$MP==""]="0"
  box$ORB=as.character(box$ORB)
  box$ORB[box$ORB==""]="0"
  box$DRB=as.character(box$DRB)
  box$DRB[box$DRB==""]="0"
  box$TRB=as.character(box$TRB)
  box$TRB[box$TRB==""]="0"
  box$AST=as.character(box$AST)
  box$AST[box$AST==""]="0"
  box$STL=as.character(box$STL)
  box$STL[box$STL==""]="0"
  box$BLK=as.character(box$BLK)
  box$BLK[box$BLK==""]="0"
  box$TOV=as.character(box$TOV)
  box$TOV[box$TOV==""]="0"
  box$PF=as.character(box$PF)
  box$PF[box$PF==""]="0"
  box$PTS=as.character(box$PTS)
  box$PTS[box$PTS==""]="0"
    
  box$team=paste("'",box$team,"'",sep="")
  box$opp_team=paste("'",box$opp_team,"'",sep="")
  box$box_score_id=paste("'",box$box_score_id,"'",sep="")  
  
  temp=box
  
  x=paste(temp,collapse = ",",sep="")
  x=apply(temp,1,function(x) { paste(x,collapse=",")})
  x=paste("(",x,")",sep="")
  
  bands <- round(seq(0,nrow(temp),length.out=(ceiling(nrow(temp)/1000)+1)))
  for (i in 1:(length(bands)-1)){
    y=x[(bands[i]+1):bands[i+1]]
    y=paste(y,collapse=",",sep="")
    text=paste("insert into college_boxscores (player,mp,fg,fga,fg_perc,x2p,x2pa,x2p_perc,x3p,x3pa,x3p_perc,ft,fta,ft_perc,orb,drb,trb,ast,stl,blk,tov,pf,pts,team_id,opp_team_id,box_score_id,year) values ",y,sep="")
    check=dbGetQuery(con,text)
    print(check)
  }
}
  

## Write Schedules into db 
load("schedules_2019.RData")  

schedules$Opponent=gsub("'","",schedules$Opponent)
schedules$Opponent=paste("'",schedules$Opponent,"'",sep="")
temp=schedules

x=paste(temp,collapse = ",",sep="")
x=apply(temp,1,function(x) { paste(x,collapse=",")})
x=paste("(",x,")",sep="")

bands <- round(seq(0,nrow(temp),length.out=(ceiling(nrow(temp)/1000)+1)))

for (i in 1:(length(bands)-1)){
  y=x[(bands[i]+1):bands[i+1]]
  y=paste(y,collapse=",",sep="")
  text=paste("insert into college_schedules (g,date,time,network,type,h_a,opponent,conf,h_a2,tm,opp,ot,w,l,streak,arena,team_id,box_score_id,opp_team_id,year) values ",y,sep="")
  check=dbGetQuery(con,text)
  print(check)
}
