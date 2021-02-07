
library(XML)
library(RCurl)
# Set Up Vars #
zz=1
year=c("2019")

## Scrape Seasons to pull back detail list fo schools ##
url <- paste("https://www.sports-reference.com/cbb/seasons/",year[zz],"-school-stats.html",sep="")
tabs <- getURL(url)
read <- readHTMLTable(tabs, stringsAsFactors = F)

teams=read$basic_school_stats
teams$tourney=""
# Older years have an asterisk
# teams$tourney[grep("\\*",as.character(teams$School))]="Y"
# teams$School=gsub("\\*","",as.character(teams$School))
teams$tourney[grep("NCAA",as.character(teams$School))]="Y"
teams$School=gsub("NCAA","",as.character(teams$School))

teams=teams[!(teams$School %in% c("Overall","School")),]

## Create PK ##
link=paste(readLines(paste("http://www.sports-reference.com/cbb/seasons/",year[zz],"-school-stats.html",sep="")),collapse=" ")

start=unlist(gregexpr("data-stat=\"school_name\" ><a href='/cbb/schools/",link))
stops=unlist(gregexpr(paste("/",year[zz],".html",sep=""),link))

xx=merge(start,stops)
xx$logic=(xx$x < xx$y)*1
xx=xx[xx$logic==1,]
xx$rank = ave (xx$y, xx$x, FUN = function(x) rank (x, ties.method ="min"))
xx=xx[xx$rank==1,]

id=c()
for(i in 1:nrow(xx)){
  test=substr(link,xx$x[i]+47,xx$y[i]-1)
  id=c(id,test)
  
}
teams$id=id
teams$year=year[zz]
teams=teams[,-17]
teams$School=gsub("'","''",teams$School)
teams$School=paste("'",teams$School,"'",sep="")
teams$tourney=paste("'",teams$tourney,"'",sep="")
teams$id=paste("'",teams$id,"'",sep="")

# Write into postgres db
# library(RPostgreSQL)
# drv=dbDriver("PostgreSQL")
# con=dbConnect(drv,user="postgres",password="sf49ers",host="localhost",port=5433,dbname="production")
# 
# bands <- round(seq(0,nrow(teams),length.out=(ceiling(nrow(teams)/1000)+1)))
# for (i in 1:(length(bands)-1)){
#   makeadance <- teams[(bands[i]+1):bands[i+1],]
#   textdata <- paste("(",apply(makeadance,1,function(x) paste(x,collapse=",")),")",collapse=",",sep="")  
#   dbGetQuery(con,paste("INSERT INTO college_teams (rk,school,g,w,l,wl_perc,srs,sos,w1,l1,w2,l2,w3,l3,tm,opp,mp,fg,fga,fg_perc,x3p,x3pa,x3p_perc,ft,fta,ft_perc,orb,trb,ast,stl,blk,tov,pf,tourney,college_id,year) values ",textdata,";",sep=""))
# }

## Rosters 
rosters=data.frame()
for(i in 1:nrow(teams)){
  
  url <- paste("https://www.sports-reference.com/cbb/schools/",gsub("'","",teams$id[i]),"/",year[zz],".html",sep="")
  tabs <- getURL(url)
  read <- readHTMLTable(tabs, stringsAsFactors = F)
  
  #read=readHTMLTable(paste("http://www.sports-reference.com/cbb/schools/",gsub("'","",teams$id[i]),"/",year[zz],".html",sep=""))  
  roster=read$roster
  link=paste(readLines(paste("http://www.sports-reference.com/cbb/schools/",gsub("'","",teams$id[i]),"/",year[zz],".html",sep="")),collapse=" ")  
  
  #link <- gsub("<U\\+[0-9A-F]{4}>", "\u03B2", link)
  #Encoding(link) <- "UTF-8"
  
  link=iconv(link,from="latin1",to="UTF-8")

  start=unlist(gregexpr("<a href='/cbb/players/",link))
  stops=unlist(gregexpr(".html'>",link))
  
  
  xx=merge(start,stops)
  xx$logic=(xx$x < xx$y)*1
  xx=xx[xx$logic==1,]
  ##xx$diff=xx$y-xx$x
  xx$rank = ave (xx$y, xx$x, FUN = function(x) rank (x, ties.method ="min"))
  xx=xx[xx$rank==1,]
  
  id=c()
  for(j in 1:nrow(xx)){
    test=substr(link,xx$x[j]+22,xx$y[j]-1)
    id=c(id,test)
    
  }
  id=unique(id)
  roster$id=id[1:nrow(roster)]
  roster$team=teams$id[i]
  roster$year=year[zz]
  
  roster=roster[,c("Player","#","Class","Pos","Height","Weight","Hometown",
                   "High School","Summary","id","team","year" )]
  
  rosters=rbind(rosters,roster)  
  
  gc()  
}

rosters$year=year[zz]

rosters$Player=gsub("'","",rosters$Player)
rosters$Player=paste("'",rosters$Player,"'",sep="")
rosters$Class=paste("'",rosters$Class,"'",sep="")
rosters$Pos=paste("'",rosters$Pos,"'",sep="")
rosters$Height=paste("'",rosters$Height,"'",sep="")
rosters$Summary=paste("'",rosters$Summary,"'",sep="")
rosters$id=paste("'",rosters$id,"'",sep="")
# rosters$team=paste("'",rosters$team,"'",sep="")

save(rosters,file="/Users/chrisgonzalez/web-scraping/college_basketball_scraper/r-data/2019_rosters.RData")
save(teams,file="/Users/chrisgonzalez/web-scraping/college_basketball_scraper/r-data/2019_teams.RData")

# Roster Inserts
# library(DBI)
# library(RPostgreSQL)
# drv=dbDriver("PostgreSQL")
# con=dbConnect(drv,user="postgres",password="sf49ers",host="localhost",port=5433,dbname="production")
# 
# bands <- round(seq(0,nrow(rosters),length.out=(ceiling(nrow(rosters)/1000)+1)))
# for (i in 1:(length(bands)-1)){
#   makeadance <- rosters[(bands[i]+1):bands[i+1],]
#   textdata <- paste("(",apply(makeadance,1,function(x) paste(x,collapse=",")),")",collapse=",",sep="")  
#   dbGetQuery(con,paste("INSERT INTO rosters (player,grad_class,pos,height,summary,player_id,college_id,year) values ",textdata,";",sep=""))
# }
# 


## Schedules
schedules=data.frame()
for(i in 1:nrow(teams)){
  
  url <- paste("https://www.sports-reference.com/cbb/schools/",gsub("'","",teams$id[i]),"/",year[zz],"-schedule.html",sep="")
  tabs <- getURL(url)
  read <- readHTMLTable(tabs, stringsAsFactors = F)
  
  #read=readHTMLTable(paste("http://www.sports-reference.com/cbb/schools/",gsub("'","",teams$id[i]),"/",year[zz],"-schedule.html",sep=""))  
  schedule=read$schedule
  schedule=schedule[schedule$Date!="Date",]
  schedule$team_id=teams$id[i]
  link=paste(readLines(paste("http://www.sports-reference.com/cbb/schools/",gsub("'","",teams$id[i]),"/",year[zz],"-schedule.html",sep="")),collapse=" ")  
  
  ## Box Id's ##
  start=unlist(gregexpr("><a href=\"/cbb/boxscores/",link))
  stops=unlist(gregexpr(".html\">",link))
  
  xx=merge(start,stops)
  xx$logic=(xx$x < xx$y)*1
  xx=xx[xx$logic==1,]
  xx$rank = ave (xx$y, xx$x, FUN = function(x) rank (x, ties.method ="min"))
  xx=xx[xx$rank==1,]
  
  id=c()
  for(j in 1:nrow(xx)){
    test=substr(link,xx$x[j]+25,xx$y[j]-1)
    id=c(id,test)
    
  }
  
  ## Opp Id's ##
  str1="data-stat=\"opp_name\" ><a href=\'/cbb/schools/"
  str2=paste("/",year[zz],".html",sep="")
  start=unlist(gregexpr(str1,link))
  stops=unlist(gregexpr(str2,link))

  xx=merge(start,stops)
  xx$logic=(xx$x < xx$y)*1
  xx=xx[xx$logic==1,]
  xx$rank = ave (xx$y, xx$x, FUN = function(x) rank (x, ties.method ="min"))
  xx=xx[xx$rank==1,]
  
  opp_id=c()
  for(j in 1:nrow(xx)){
    test=substr(link,xx$x[j]+nchar(str1),xx$y[j]-1)
    opp_id=c(opp_id,test)
    
  }
  
  
  id=unique(id)
  if(nrow(schedule)!=length(id)){
    schedule=schedule[1:ifelse(nrow(schedule)>=length(id),length(id),nrow(schedule)),]
  }
  schedule$id=id
  schedule$team_id=gsub("'","",teams$id[i])
  
  schedule$opp_team_id=""
  schedule$opp_team_id[schedule$Conf!=""]=opp_id
  
  schedules=rbind(schedules,schedule)  
  
}
schedules$year=year[zz]
schedules1=schedules

schedules$Time=""
schedules$Network=""

# 2014 and Less
colnames(schedules)=c("G","Date","Time","Type","h_a","Opponent","Conf","h_a2","Tm","Opp",
                     "OT","W","L","Streak","Arena","team_id","id","opp_team_id","year","Network")

# 2015 and New
 colnames(schedules)=c("G","Date","Time","Network","Type","h_a","Opponent","Conf","h_a2","Tm","Opp",
                       "OT","W","L","Streak","Arena","team_id","id","opp_team_id","year")

schedules=schedules[,c("G","Date","Time","Network","Type","h_a","Opponent","Conf","h_a2","Tm","Opp",
                       "OT","W","L","Streak","Arena","team_id","id","opp_team_id","year")]

schedules$Date=paste("'",schedules$Date,"'",sep="")
schedules$Time=paste("'",schedules$Time,"'",sep="")
schedules$Network=paste("'",schedules$Network,"'",sep="")
schedules$Type=paste("'",schedules$Type,"'",sep="")
schedules$h_a=paste("'",schedules$h_a,"'",sep="")

schedules$Opponent=gsub("'","",schedules$Opponent)
schedules$Opponent=paste("'",schedules$Opponent,"'",sep="")
schedules$Conf=paste("'",schedules$Conf,"'",sep="")
schedules$h_a2=paste("'",schedules$h_a2,"'",sep="")
schedules$Opponent=paste("'",schedules$Opponent,"'",sep="")
schedules$OT=paste("'",schedules$OT,"'",sep="")
schedules$Streak=paste("'",schedules$Streak,"'",sep="")
schedules$Arena=gsub("'","",schedules$Arena)
schedules$Arena=paste("'",schedules$Arena,"'",sep="")
schedules$team_id=paste("'",schedules$team_id,"'",sep="")
schedules$id=paste("'",schedules$id,"'",sep="")
schedules$opp_team_id=paste("'",schedules$opp_team_id,"'",sep="")

save(schedules,file="/Users/chrisgonzalez/web-scraping/college_basketball_scraper/r-data/schedules_2019.RData")

# Schedules Inserts 
# library(RPostgreSQL)
# drv=dbDriver("PostgreSQL")
# con=dbConnect(drv,user="postgres",password="sf49ers",host="localhost",port=5433,dbname="production")
# 
# bands <- round(seq(0,nrow(schedules),length.out=(ceiling(nrow(schedules)/1000)+1)))
# for (i in 1:(length(bands)-1)){
#   makeadance <- schedules[(bands[i]+1):bands[i+1],]
#   textdata <- paste("(",apply(makeadance,1,function(x) paste(x,collapse=",")),")",collapse=",",sep="")  
#   dbGetQuery(con,paste("INSERT INTO schedules (g,date,time,network,type,h_a,opponent,conference,h_a2,tm,opp,ot,w,l,streak,arena,team_id,box_score_id,year) values ",textdata,";",sep=""))
# }
# 



## Box Scores 

count=1
box=data.frame()
for(i in 667:nrow(schedules)){
  url <- paste("https://www.sports-reference.com/cbb/boxscores/",gsub("'","",schedules$id[i]),".html",sep="")
  tabs <- getURL(url)
  read <- readHTMLTable(tabs, stringsAsFactors = F)
  
  #read=readHTMLTable(paste("http://www.sports-reference.com/cbb/boxscores/",gsub("'","",schedules$id[i]),".html",sep=""))  
  n=names(read)
  n=n[grep("box-score-basic",n)]
  read=read[n]
  for(k in 1:length(read)){
    boxes=read[[k]]
    boxes$team=n[k]
    boxes$opp_team=n[!(n %in% n[k])]
    boxes$box_score_id=gsub("'","",schedules$id[i])
    boxes$year=year[zz]
    
    colnames(boxes)=c("Starters","MP","FG","FGA","FG%","2P","2PA","2P%","3P","3PA","3P%","FT","FTA","FT%","ORB","DRB",
                      "TRB","AST","STL","BLK","TOV","PF","PTS","team","opp_team","box_score_id","year")
    box=rbind(box,boxes)
  }
  gc()
  
  if(nrow(box)>10000){
    save(box,file=paste("/Users/chrisgonzalez/web-scraping/college_basketball_scraper/r-data/",year[zz],"_pt",count,".RData",sep=""))
    # save(i,file="/Users/chrisgonzalez/web-scraping/college_basketball_scraper/r-data/boxscores_2019.RData")
    count=count+1
    box=data.frame()
    gc()
  }
  
}
