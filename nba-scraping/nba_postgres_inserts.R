library(RPostgreSQL)
drv <- dbDriver("PostgreSQL")
con <- dbConnect(drv, dbname="basketball",user="postgres",password="estarguars",host = "localhost", port = 5432)

load("/Users/chrisgonzalez/web-scraping/nba-scraping/r-data/player_key.RData")

temp=player_key
temp$euro=gsub("players/","",temp$euro)


temp$nba=paste("'",temp$nba,"'",sep="")
temp$college=paste("'",temp$college,"'",sep="")
temp$euro=paste("'",temp$euro,"'",sep="")

x=paste(temp,collapse = ",",sep="")
x=apply(temp,1,function(x) { paste(x,collapse=",")})
x=paste("(",x,")",sep="")
x=paste(x,collapse=",",sep="")

text=paste("insert into nba_college_key(nba,college,euro) values ",x,sep="")

check=dbGetQuery(con,text)


# Inserted Player Key 
# NBA Seasons Inserted Here  
load("/Users/chrisgonzalez/web-scraping/nba-scraping/r-data/teams.RData")
final_data$team=paste("'",final_data$team,"'",sep="")
final_data$gb=as.character(final_data$gb)
final_data$gb[final_data$gb=="—"]="0"

final_data$conf=paste("'",final_data$conf,"'",sep="")
final_data$team_id=paste("'",final_data$team_id,"'",sep="")

temp=final_data

x=paste(temp,collapse = ",",sep="")
x=apply(temp,1,function(x) { paste(x,collapse=",")})
x=paste("(",x,")",sep="")

x=paste(x,collapse=",",sep="")

text=paste("insert into nba_seasons(team,wins,losses,w_l_perc,gb,pts_g,pa_g,srs,conf,year,team_id) values ",x,sep="")

check=dbGetQuery(con,text)


## Schedules Insert Here 
## Need Bands Code 
## Loaded as Temp from nba_schedules
load("/Users/chrisgonzalez/web-scraping/nba-scraping/r-data/schedules.RData")
colnames(temp)=c("g","date","time","network","box_score","home_away","opponent","outcome","game_length","team_score","opp_score","wins","losses","streak","notes","team_id","year","game_type","box_score_id","opp_team_id")

temp$date=paste("'",temp$date,"'",sep="")
temp$time=paste("'",temp$time,"'",sep="")
temp$network=paste("'",temp$network,"'",sep="")
temp$box_score=paste("'",temp$box_score,"'",sep="")

temp$home_away=paste("'",temp$home_away,"'",sep="")
temp$opponent=paste("'",temp$opponent,"'",sep="")
temp$outcome=paste("'",temp$outcome,"'",sep="")
temp$game_length=paste("'",temp$game_length,"'",sep="")

temp$streak=paste("'",temp$streak,"'",sep="")
temp$notes=gsub("'","''",temp$notes)
temp$notes=paste("'",temp$notes,"'",sep="")
temp$team_id=paste("'",temp$team_id,"'",sep="")

temp$game_type=paste("'",temp$game_type,"'",sep="")
temp$box_score_id=paste("'",temp$box_score_id,"'",sep="")
temp$opp_team_id=paste("'",temp$opp_team_id,"'",sep="")


x=paste(temp,collapse = ",",sep="")
x=apply(temp,1,function(x) { paste(x,collapse=",")})
x=paste("(",x,")",sep="")

bands <- round(seq(0,nrow(temp),length.out=(ceiling(nrow(temp)/1000)+1)))

for (i in 1:(length(bands)-1)){
  y=x[(bands[i]+1):bands[i+1]]
  y=paste(y,collapse=",",sep="")
  text=paste("insert into nba_schedules(g,date,time,network,boxscore,home_away,opponent,outcome,game_length,team_score,opp_score,wins,losses,streak,notes,team_id,year,game_type,box_score_id,opp_team_id) values ",y,sep="")
  check=dbGetQuery(con,text)

  }


## Rosters Then All box scores left
load("/Users/chrisgonzalez/web-scraping/nba-scraping/r-data/roster.RData")
roster$name=gsub("'","''",roster$name)
roster$school=gsub("'","''",roster$school)

roster$number=paste("'",roster$number,"'",sep="")
roster$name=paste("'",roster$name,"'",sep="")
roster$pos=paste("'",roster$pos,"'",sep="")
roster$height=paste("'",roster$height,"'",sep="")
roster$weight=paste("'",roster$weight,"'",sep="")
roster$bday=paste("'",roster$bday,"'",sep="")
roster$country=paste("'",roster$country,"'",sep="")
roster$yrs_pro=paste("'",roster$yrs_pro,"'",sep="")
roster$school=paste("'",roster$school,"'",sep="")
roster$id=paste("'",roster$id,"'",sep="")
roster$team=paste("'",roster$team,"'",sep="")

temp=roster

x=paste(temp,collapse = ",",sep="")
x=apply(temp,1,function(x) { paste(x,collapse=",")})
x=paste("(",x,")",sep="")

bands <- round(seq(0,nrow(temp),length.out=(ceiling(nrow(temp)/1000)+1)))

for (i in 1:(length(bands)-1)){
  y=x[(bands[i]+1):bands[i+1]]
  y=paste(y,collapse=",",sep="")
  text=paste("insert into nba_rosters(number,name,pos,height,weight,bday,country,yrs_pro,school,player_id,year,team) values ",y,sep="")
  check=dbGetQuery(con,text)
  
}


## Box Scores Upload 

# rows=c()
# files=c("nba_box_scores44911.RData","nba_box_scores5000.RData","nba_box_scores10000.RData","nba_box_scores15000.RData","nba_box_scores20000.RData","nba_box_scores25000.RData","nba_box_scores30000.RData","nba_box_scores35000.RData","nba_box_scores40000.RData")
# 
# for(j in 1:length(files)){

# load(files[j])

load("/Users/chrisgonzalez/web-scraping/nba-scraping/r-data/boxscores.RData")

boxscores$player=gsub("'","''",boxscores$player)
boxscores$player=paste("'",boxscores$player,"'",sep="")

boxscores$mp=as.character(boxscores$mp)
boxscores$mp=gsub(":",".",boxscores$mp)
boxscores$mp[boxscores$mp==""]="0"

boxscores$fg=as.character(boxscores$fg)
boxscores$fg[boxscores$fg==""]="0"
boxscores$fga=as.character(boxscores$fga)
boxscores$fga[boxscores$fga==""]="0"

boxscores$fg_perc=as.character(boxscores$fg_perc)
boxscores$fg_perc[boxscores$fg_perc==""]="0"
boxscores$x3p=as.character(boxscores$x3p)
boxscores$x3p[boxscores$x3p==""]="0"
boxscores$x3pa=as.character(boxscores$x3pa)
boxscores$x3pa[boxscores$x3pa==""]="0"
boxscores$x3p_perc=as.character(boxscores$x3p_perc)
boxscores$x3p_perc[boxscores$x3p_perc==""]="0"
boxscores$ft=as.character(boxscores$ft)
boxscores$ft[boxscores$ft==""]="0"
boxscores$fta=as.character(boxscores$fta)
boxscores$fta[boxscores$fta==""]="0"
boxscores$ft_perc=as.character(boxscores$ft_perc)
boxscores$ft_perc[boxscores$ft_perc==""]="0"

boxscores$orb=as.character(boxscores$orb)
boxscores$orb[boxscores$orb==""]="0"
boxscores$drb=as.character(boxscores$drb)
boxscores$drb[boxscores$drb==""]="0"
boxscores$trb=as.character(boxscores$trb)
boxscores$trb[boxscores$trb==""]="0"
boxscores$ast=as.character(boxscores$ast)
boxscores$ast[boxscores$ast==""]="0"
boxscores$stl=as.character(boxscores$stl)
boxscores$stl[boxscores$stl==""]="0"
boxscores$blk=as.character(boxscores$blk)
boxscores$blk[boxscores$blk==""]="0"
boxscores$tov=as.character(boxscores$tov)
boxscores$tov[boxscores$tov==""]="0"
boxscores$pf=as.character(boxscores$pf)
boxscores$pf[boxscores$pf==""]="0"
boxscores$pts=as.character(boxscores$pts)
boxscores$pts[boxscores$pts==""]="0"

boxscores$team=paste("'",boxscores$team,"'",sep="")
boxscores$player_id=paste("'",boxscores$player_id,"'",sep="")
boxscores$box_id=paste("'",boxscores$box_id,"'",sep="")

boxscores=boxscores[boxscores$mp!="Did Not Play",]
boxscores=boxscores[boxscores$mp!="Player Suspended",]

boxscores=boxscores[boxscores$mp!="Not With Team",]
boxscores=boxscores[boxscores$mp!="Did Not Dress",]

temp=boxscores
x=paste(temp,collapse = ",",sep="")
x=apply(temp,1,function(x) { paste(x,collapse=",")})
x=paste("(",x,")",sep="")

bands <- round(seq(0,nrow(temp),length.out=(ceiling(nrow(temp)/1000)+1)))

for (i in 1:(length(bands)-1)){
  y=x[(bands[i]+1):bands[i+1]]
  y=paste(y,collapse=",",sep="")
  text=paste("insert into nba_boxscores(player,mp,fg,fga,fg_perc,x3p,x3pa,x3p_perc,ft,fta,ft_perc,orb,drb,trb,ast,stl,blk,tov,pf,pts,team,player_id,box_id) values ",y,sep="")
  check=dbGetQuery(con,text)
  
}

# }




### College Next 



bands <- round(seq(0,nrow(sqldata),length.out=(ceiling(nrow(sqldata)/1000)+1)))
for (i in 1:(length(bands)-1)){
  makeadance <- sqldata[(bands[i]+1):bands[i+1],]


