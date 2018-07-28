# setwd("H:/Downloads/basketball/")

library(XML)
library(RCurl)
# Set Up Vars #
# zz=1
# year=c("2017")

year=seq(2018,2018,by=1)
year=as.character(year)

final_data=data.frame()
for(zz in 1:length(year)){

## Scrape Team Data ##
  
  # url="https://www.basketball-reference.com/leagues/NBA_1980.html"
  
url=paste("https://www.basketball-reference.com/leagues/NBA_",year[zz],".html",sep="")
tabs=getURL(url)  
read=readHTMLTable(tabs)

link=paste(readLines(paste("http://www.basketball-reference.com/leagues/NBA_",year[zz],".html",sep="")),collapse=" ")


east=read[[1]]
west=read[[2]]

east$conf="east"
west$conf="west"
colnames(east)=c("team","wins","losses","w_l_perc","gb","pts_g","pa_g","srs","conf")
colnames(west)=c("team","wins","losses","w_l_perc","gb","pts_g","pa_g","srs","conf")
east=east[!(is.na(east$wins)),]
west=west[!(is.na(west$wins)),]

data=rbind(east,west)
data$year=year[zz]

char1="data-stat=\"team_name\" ><a href=\"/teams/"
char2=paste(year[zz],".html",sep="")

start=unlist(gregexpr(char1,link))
stops=unlist(gregexpr(char2,link))

xx=merge(start,stops)
xx$logic=(xx$x < xx$y)*1
xx=xx[xx$logic==1,]
xx$rank = ave (xx$y, xx$x, FUN = function(x) rank (x, ties.method ="min"))
xx=xx[xx$rank==1,]

id=c()
for(i in 1:nrow(xx)){
  test=substr(link,xx$x[i]+nchar(char1),xx$y[i]-2)
  id=c(id,test)
  
}
data$team_id=id[1:nrow(data)]


final_data=rbind(final_data,data)

}


# Roster Info 
roster=data.frame()
for(i in 1:nrow(final_data)){
  
  url=paste("https://www.basketball-reference.com/teams/",final_data$team_id[i],"/",final_data$year[i],".html",sep="")
  tabs=getURL(url)  
  
  read=readHTMLTable(tabs)
  
  rosters=read[[1]]
  
  link=paste(readLines(paste("https://www.basketball-reference.com/teams/",final_data$team_id[i],"/",final_data$year[i],".html",sep="")),collapse=" ")
  
  char1="data-append-csv=\""
  char2="\" "
  start=unlist(gregexpr(char1,link))
  stops=unlist(gregexpr(char2,link))
  
  xx=merge(start,stops)
  xx$logic=(xx$x < xx$y)*1
  xx=xx[xx$logic==1,]
  xx$rank = ave (xx$y, xx$x, FUN = function(x) rank (x, ties.method ="min"))
  xx=xx[xx$rank==1,]
  
  id=c()
  for(k in 1:nrow(xx)){
    test=substr(link,xx$x[k]+nchar(char1),xx$y[k]-1)
    id=c(id,test)
    
  }
  id=unique(id)
  rosters$id=id[1:nrow(rosters)]
  rosters$year=final_data$year[i]
  rosters$team_id=final_data$team_id[i]
  
  colnames(rosters)=colnames(roster)
 roster=rbind(roster,rosters)
}

colnames(roster)=c("number","name","pos","height","weight","bday","country","yrs_pro","school","id","year","team")

## create box_score scripts and player profile scripts to match to college data 

save(roster,file="nba_roster.RData")
save(final_data,file="nba_teams.RData")


schedule=data.frame()
temp=data.frame()

for(i in 1:nrow(final_data)){
  url=paste("https://www.basketball-reference.com/teams/",final_data$team_id[i],"/",final_data$year[i],"_games.html",sep="")
  tabs=getURL(url)  
  read=readHTMLTable(tabs)
  
  link=paste(readLines(url),collapse=" ")
  
  for(j in 1:length(read)){
    schedules=read[[j]]
    schedules$team=final_data$team_id[i]
    schedules$year=final_data$year[i]
    schedules=schedules[schedules$Date!="Date",]
    if(j==1){
      schedules$type="reg_season"
    }
    if(j==2){
      schedules$type="playoffs"
    }
    schedule=rbind(schedule,schedules)
  }
  
  # Box ID   
  char1="><a href=\"/boxscores/"
  char2=".html"
  start=unlist(gregexpr(char1,link))
  stops=unlist(gregexpr(char2,link))
  
  xx=merge(start,stops)
  xx$logic=(xx$x < xx$y)*1
  xx=xx[xx$logic==1,]
  xx$rank = ave (xx$y, xx$x, FUN = function(x) rank (x, ties.method ="min"))
  xx=xx[xx$rank==1,]
  
  id=c()
  for(k in 1:nrow(xx)){
    test=substr(link,xx$x[k]+nchar(char1),xx$y[k]-1)
    id=c(id,test)
    
  }
  id=id[nchar(id)<13]
  id=unique(id)
  schedule$box_id=id

  # Opp Team Id
  
  link=paste(readLines(url),collapse=" ")
  char1="><a href=\"/teams/"
  char2=paste("/",final_data$year[i],".html\">",sep="")
  start=unlist(gregexpr(char1,link))
  stops=unlist(gregexpr(char2,link))
  
  xx=merge(start,stops)
  xx$logic=(xx$x < xx$y)*1
  xx=xx[xx$logic==1,]
  xx$rank = ave (xx$y, xx$x, FUN = function(x) rank (x, ties.method ="min"))
  xx=xx[xx$rank==1,]
  
  id=c()
  for(k in 1:nrow(xx)){
    test=substr(link,xx$x[k]+nchar(char1),xx$y[k]-1)
    id=c(id,test)
    
  }
  id=id[nchar(id)<4]
  id=id[id!=final_data$team_id[i]]
  schedule$opp_team_id=id
  
  temp=rbind(temp,schedule)
  schedule=data.frame()
  

}
  
  
save(temp,file="nba_schedules.RData")


p=data.frame(unique(roster[,c(2,10)]))
p$first_letter=substr(p$id,1,1)
colnames(p)=c("name","id","first_letter")
# p=p[p$id %in% roster$id[roster$year %in% c("2011","2012","2013","2014","2015","2016","2017")],]

player_key=data.frame()
for(i in 463:nrow(p)){
  url=paste("https://www.basketball-reference.com/players/",p$first_letter[i],"/",p$id[i],".html",sep="")
  tabs=getURL(url)  
  read=readHTMLTable(tabs)
  
  link=paste(readLines(url,encoding = "UTF-8"),collapse=" ")
  
  # College Scraper 
  char1="<a href=\"https://www.sports-reference.com/cbb/players/"
  char2=".html\">"
  start=unlist(gregexpr(char1,link))
  stops=unlist(gregexpr(char2,link))
  
  if(start!=-1){
  xx=merge(start,stops)
  xx$logic=(xx$x < xx$y)*1
  xx=xx[xx$logic==1,]
  xx$rank = ave (xx$y, xx$x, FUN = function(x) rank (x, ties.method ="min"))
  xx=xx[xx$rank==1,]

  id=c()
  for(k in 1:1){
    test=substr(link,xx$x[k]+nchar(char1),xx$y[k]-1)
    id=c(id,test)
    
  }
  college=unique(id)
  }else{college=""}

  # Euro Scraper 
  char1="<a href=\"https://www.basketball-reference.com/euro/"
  char2=".html\">"
  start=unlist(gregexpr(char1,link))
  stops=unlist(gregexpr(char2,link))
  
  if(start!=-1){
  xx=merge(start,stops)
  xx$logic=(xx$x < xx$y)*1
  xx=xx[xx$logic==1,]
  xx$rank = ave (xx$y, xx$x, FUN = function(x) rank (x, ties.method ="min"))
  xx=xx[xx$rank==1,]
  
  id=c()
  for(k in 1:nrow(xx)){
    test=substr(link,xx$x[k]+nchar(char1),xx$y[k]-1)
    id=c(id,test)
    
  }
  euro=unique(id)
  
  }else{euro=""}
  
  player_key=rbind(player_key,data.frame(nba=p$id[i],college=college,euro=euro))
}  


save(player_key,file="nba_player_key.RData")  


load("nba_roster.RData")
load("nba_teams.RData")
load("nba_schedules.RData")
load("nba_player_key.RData")


games=unique(temp$box_id)
boxscores=data.frame()
for(i in 217:length(games)){
  url=paste("https://www.basketball-reference.com/boxscores/",games[i],".html",sep="")
  tabs=getURL(url)  
  read=readHTMLTable(tabs)
  
  link=paste(readLines(url,encoding = "UTF-8"),collapse=" ")
  
  # Player Id Scraper 
  char1="data-append-csv=\""
  char2="\" data-stat=\"player\""
  start=unlist(gregexpr(char1,link))
  stops=unlist(gregexpr(char2,link))
  
  xx=merge(start,stops)
  xx$logic=(xx$x < xx$y)*1
  xx=xx[xx$logic==1,]
  xx$rank = ave (xx$y, xx$x, FUN = function(x) rank (x, ties.method ="min"))
  xx=xx[xx$rank==1,]
  
  id=c()
  for(k in 1:nrow(xx)){
    test=substr(link,xx$x[k]+nchar(char1),xx$y[k]-1)
    id=c(id,test)
    
  }
id=unique(id)  
  names=names(read)[grep("box",names(read))] 
  names=names[grep("basic",names)] 
  temp1=data.frame(read[names[1]])
  temp2=data.frame(read[names[2]])
  temp1=temp1[temp1[,2]!="MP",]
  temp2=temp2[temp2[,2]!="MP",]
  
  temp1$team=names[1]
  temp2$team=names[2]
  temp1$player_id=id[1:nrow(temp1)]
  temp2$player_id=id[(nrow(temp1)+1):length(id)]
  temp1$box_id=games[i]
  temp2$box_id=games[i]
  
  temp1=temp1[,!(grepl("\\.\\.\\.",colnames(temp1)))]
  temp2=temp2[,!(grepl("\\.\\.\\.",colnames(temp2)))]
  
  colnames(temp1)=c("player","mp","fg","fga","fg_perc","x3p","x3pa","x3p_perc","ft","fta","ft_perc","orb","drb","trb",
                    "ast","stl","blk","tov","pf","pts","team","player_id","box_id")
  colnames(temp2)=c("player","mp","fg","fga","fg_perc","x3p","x3pa","x3p_perc","ft","fta","ft_perc","orb","drb","trb",
                    "ast","stl","blk","tov","pf","pts","team","player_id","box_id")
  
  boxscores=rbind(boxscores,temp1,temp2)
  gc()
  print(Sys.time())

  if(i%%5000==0){
    save(boxscores,file=paste("nba_box_scores",i,".RData",sep=""))
    boxscores=data.frame()
  }
  
  }  
  
save(boxscores,file="/Users/chrisgonzalez/web-scraping/nba-scraping/r-data/boxscores.RData")
save(roster,file="/Users/chrisgonzalez/web-scraping/nba-scraping/r-data/roster.RData")
save(final_data,file="/Users/chrisgonzalez/web-scraping/nba-scraping/r-data/teams.RData")
save(temp,file="/Users/chrisgonzalez/web-scraping/nba-scraping/r-data/schedules.RData")
save(player_key,file="/Users/chrisgonzalez/web-scraping/nba-scraping/r-data/player_key.RData")



  #https://www.basketball-reference.com/boxscores/201706120GSW.html
  
  
  