

final=data.frame()
for(j in 1:32){

  link=readLines(paste("https://www.usnews.com/best-colleges/rankings/national-universities?_page=",j,sep=""))
  link=paste(link,collapse = "")
  
  # School Search 
  
  char1=",\"displayName\":\""
  char2="\",\"sortName\""
  
  start=unlist(gregexpr(char1,link))
  stops=unlist(gregexpr(char2,link))
  
  xx=merge(start,stops)
  xx$logic=(xx$x < xx$y)*1
  xx=xx[xx$logic==1,]
  xx$rank = ave (xx$y, xx$x, FUN = function(x) rank (x, ties.method ="min"))
  xx=xx[xx$rank==1,]
  
  school_id=c()
  for(i in 1:nrow(xx)){
    test=substr(link,xx$x[i]+nchar(char1),xx$y[i]-1)
    school_id=c(school_id,test)
  }
  
  school_id=school_id[!grepl("National Universities",school_id)]
  
  
  # State
  char1=",\"state\":\""
  char2="\",\"city\":\""
  
  start=unlist(gregexpr(char1,link))
  stops=unlist(gregexpr(char2,link))
  
  xx=merge(start,stops)
  xx$logic=(xx$x < xx$y)*1
  xx=xx[xx$logic==1,]
  xx$rank = ave (xx$y, xx$x, FUN = function(x) rank (x, ties.method ="min"))
  xx=xx[xx$rank==1,]
  
  state=c()
  for(i in 1:nrow(xx)){
    test=substr(link,xx$x[i]+nchar(char1),xx$y[i]-1)
    state=c(state,test)
  }
  
  
  # City
  char1="\",\"city\":\""
  char2="\",\"zip\":\""
  
  start=unlist(gregexpr(char1,link))
  stops=unlist(gregexpr(char2,link))
  
  xx=merge(start,stops)
  xx$logic=(xx$x < xx$y)*1
  xx=xx[xx$logic==1,]
  xx$rank = ave (xx$y, xx$x, FUN = function(x) rank (x, ties.method ="min"))
  xx=xx[xx$rank==1,]
  
  city=c()
  for(i in 1:nrow(xx)){
    test=substr(link,xx$x[i]+nchar(char1),xx$y[i]-1)
    city=c(city,test)
  }
  
  
  # Zip
  char1="\",\"zip\":\""
  char2="\",\"region\""
  
  start=unlist(gregexpr(char1,link))
  stops=unlist(gregexpr(char2,link))
  
  xx=merge(start,stops)
  xx$logic=(xx$x < xx$y)*1
  xx=xx[xx$logic==1,]
  xx$rank = ave (xx$y, xx$x, FUN = function(x) rank (x, ties.method ="min"))
  xx=xx[xx$rank==1,]
  
  zip=c()
  for(i in 1:nrow(xx)){
    test=substr(link,xx$x[i]+nchar(char1),xx$y[i]-1)
    zip=c(zip,test)
  }
  
  
  # Rank
  char1="\"rankingDisplayRank\":\"#"
  char2="\",\"rankingDisplayScore\""
  
  start=unlist(gregexpr(char1,link))
  stops=unlist(gregexpr(char2,link))
  
  xx=merge(start,stops)
  xx$logic=(xx$x < xx$y)*1
  xx=xx[xx$logic==1,]
  xx$rank = ave (xx$y, xx$x, FUN = function(x) rank (x, ties.method ="min"))
  xx=xx[xx$rank==1,]
  
  rank=c()
  for(i in 1:nrow(xx)){
    test=substr(link,xx$x[i]+nchar(char1),xx$y[i]-1)
    rank=c(rank,test)
  }
  
college=data.frame(school=school_id,city=city,state=state,zip=zip,rank=rank,page=j)
final=rbind(final,college)
  
  }

final=unique(final)

