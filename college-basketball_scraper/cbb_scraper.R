setwd("/Users/chrisgonzalez/Documents/web-scraping/college-basketball_scraper/")

library(XML)
library(RCurl)

substring_patterns <- function(text,pattern1,pattern2) {
  href=substr(text,regexpr(pattern1,text )+nchar(pattern1),regexpr(pattern2,text)-1)
  return(href)
}

webpage_min_chars_between <- function(text,pattern1,pattern2){
  start=unlist(gregexpr(pattern1,text))
  stops=unlist(gregexpr(pattern2,text))
  
  if(start[1]==-1 | stops[1]==-1){
    return("")
  }
  
  xx=merge(start,stops)
  xx$logic=(xx$x < xx$y)*1
  xx=xx[xx$logic==1,]
  xx$rank = ave (xx$y, xx$x, FUN = function(x) rank (x, ties.method ="min"))
  xx=xx[xx$rank==1,]
  
  id=c()
  for(j in 1:nrow(xx)){
    test=substr(link,xx$x[j],xx$y[j]-1)
    id=c(id,test)
  }
  return(id)
}


# Set Up Vars #
year=seq(2005,2022)
years_df=data.frame()

for(zz in 1:length(year)){
  print(zz)
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
  teams=teams[ , colnames(teams)[make.names(colnames(teams))!="X."] ]
  teams$School=gsub("'","''",teams$School)
  teams$School=paste("'",teams$School,"'",sep="")
  teams$tourney=paste("'",teams$tourney,"'",sep="")
  teams$id=paste("'",teams$id,"'",sep="")
  
  years_df=rbind(years_df,teams)
}
  
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
for(i in 1:nrow(years_df)){
  print(i)
  
  url <- paste("https://www.sports-reference.com/cbb/schools/",gsub("'","",years_df$id[i]),"/",years_df$year[i],".html",sep="")
  tabs <- getURL(url)
  read <- readHTMLTable(tabs, stringsAsFactors = F)
  if(length(read)==0){
    next
    }
  
  #read=readHTMLTable(paste("http://www.sports-reference.com/cbb/schools/",gsub("'","",teams$id[i]),"/",year[zz],".html",sep=""))  
  roster=read$roster
  link=paste(readLines(paste("http://www.sports-reference.com/cbb/schools/",gsub("'","",years_df$id[i]),"/",years_df$year[i],".html",sep="")),collapse=" ")  
  
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
  roster$team=years_df$id[i]
  roster$year=years_df$year[i]
  
  roster=roster[,c("Player","#","Class","Pos","Height","Weight","Hometown",
                   "id","team","year" )]
  
  rosters=rbind(rosters,roster)  
  
  gc()  
}

rosters$Player=gsub("'","",rosters$Player)
rosters$Player=paste("'",rosters$Player,"'",sep="")
rosters$Class=paste("'",rosters$Class,"'",sep="")
rosters$Pos=paste("'",rosters$Pos,"'",sep="")
rosters$Height=paste("'",rosters$Height,"'",sep="")
rosters$id=paste("'",rosters$id,"'",sep="")
# rosters$team=paste("'",rosters$team,"'",sep="")

save(rosters,file="r-data/cbb_rosters.RData")
save(years_df,file="r-data/cbb_teams_years.RData")

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
for(i in 5601:nrow(years_df)){
  print(i)
  url <- paste("https://www.sports-reference.com/cbb/schools/",gsub("'","",years_df$id[i]),"/",years_df$year[i],"-schedule.html",sep="")
  tabs <- getURL(url)
  read <- readHTMLTable(tabs, stringsAsFactors = F)
  if(length(read)==0){
    next
  }
  
  
  #read=readHTMLTable(paste("http://www.sports-reference.com/cbb/schools/",gsub("'","",teams$id[i]),"/",year[zz],"-schedule.html",sep=""))  
  schedule=read$schedule
  schedule=schedule[,!(colnames(schedule) %in% c("Time","Network"))]
  
  schedule=schedule[schedule$Date!="Date",]
  schedule$team_id=years_df$id[i]
  
  link=paste(readLines(paste("http://www.sports-reference.com/cbb/schools/",gsub("'","",years_df$id[i]),"/",years_df$year[i],"-schedule.html",sep="")),collapse=" ")  
  
  ## Box Id's ##
  id=webpage_min_chars_between(link,"date_game","</td>")
  id=id[nchar(id) < 150]
  href=substring_patterns(id,"<a href=\"/cbb/boxscores/",".html") ## use R function here 
  schedule$boxscore_id=href
  
  ## Opp Id's ##
  opp_id=webpage_min_chars_between(link,"opp_name","</td>")
  opp_id=opp_id[nchar(opp_id) < 150]
  href=substring_patterns(opp_id,"opp_name\" ><a href='/cbb/schools/",paste("/",years_df$year[i],".html",sep="") ) ## use R function here 
  schedule$opp_team_id=href
  
  schedule$year=years_df$year[i]
  if(class(schedule)=="list"){
    next
  }
  
  colnames(schedule)=c("G","Date","Type","h_a","Opponent","Conf","w_l","Tm","Opp",
                        "OT","W","L","Streak","Arena","team_id","boxscore_id","opp_team_id",
                        "year")
  
  schedules=rbind(schedules,schedule)  
}

save(schedules,file="r-data/cbb_schedules.RData")

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

boxscore_ids=unique(schedules$boxscore_id)
boxscore_ids=boxscore_ids[boxscore_ids!=""]
box=data.frame()
for(i in 1:length(boxscore_ids) ){
  print(i)
  url <- paste("https://www.sports-reference.com/cbb/boxscores/",gsub("'","",boxscore_ids[i]),".html",sep="")
  tabs <- getURL(url)
  read <- readHTMLTable(tabs, stringsAsFactors = F)
  
  #read=readHTMLTable(paste("http://www.sports-reference.com/cbb/boxscores/",gsub("'","",schedules$id[i]),".html",sep=""))  
  n=names(read)
  n=n[grep("box-score-basic",n)]
  read=read[n]
  for(k in 1:length(read)){
    link=paste(readLines(url),collapse=" ")  
    #link=webpage_min_chars_between(link,n[k],"</table>")
    link=webpage_min_chars_between(link,paste("id=\"",n[k],"\"",sep=""),"</table>")
    
    ## player ids
    #href=webpage_min_chars_between(link[1],"<a href=\"/cbb/players/","</a>")
    
    link[1]=webpage_min_chars_between(link[1],"<tbody>","</tbody>")
    href=webpage_min_chars_between(link[1],"data-stat=\"player\" ","</th>")
    #href=href[grepl("href",href)]
    href=substring_patterns(href,"<a href=\"/cbb/players/",".html")
    
    boxes=read[[k]]
    boxes$team=n[k]
    boxes$box_score_id=boxscore_ids[i]

    
    if(length(href)==0){
      boxes$player_id=""
    }
    else{
      boxes$player_id=href   
    }
    boxes=boxes[boxes$MP!="MP",]

    colnames(boxes)=c("Starters","MP","FG","FGA","FG%","2P","2PA","2P%","3P","3PA","3P%","FT","FTA","FT%","ORB","DRB",
                      "TRB","AST","STL","BLK","TOV","PF","PTS","team","box_score_id","player_id")
    box=rbind(box,boxes)
  }
  gc()
  
  if(nrow(box)>100000 | i==length(boxscore_ids)){
    save(box,file=paste("r-data/boxscores_",i,".RData",sep=""))
    box=data.frame()
    gc()
    print(paste('saved at ',i))
  }
  
}
