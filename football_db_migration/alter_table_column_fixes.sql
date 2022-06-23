
## NFL Boxscore defense block

begin transaction
	ALTER TABLE nfl_boxscore_defense 
	RENAME COLUMN box_score_id TO boxscore_href;

	alter table nfl_boxscore_defense
	add column player_id text,
	add column boxscore_id text;

	update nfl_boxscore_defense 
	set 
	player_id = replace(
		replace(
			SUBSTRING(replace(player_href,'/players/','') FROM POSITION('/' IN replace(player_href,'/players/',''))) 
		,'/','')
	,'.htm',''),
	
	boxscore_id=replace(replace(boxscore_href,'/boxscores/',''),'.htm','');

rollback
--commit

### block ends here ###


## NFL Boxscore kick_returns block
begin transaction
	ALTER TABLE nfl_boxscore_kick_returns 
	RENAME COLUMN box_score_id TO boxscore_href;

	alter table nfl_boxscore_kick_returns
	add column player_id text,
	add column boxscore_id text;

	update nfl_boxscore_kick_returns 
	set 
	player_id = replace(
		replace(
			SUBSTRING(replace(player_href,'/players/','') FROM POSITION('/' IN replace(player_href,'/players/',''))) 
		,'/','')
	,'.htm',''),
	
	boxscore_id=replace(replace(boxscore_href,'/boxscores/',''),'.htm','');

rollback
--commit
### block ends here ###



## NFL Boxscore kicking block
begin transaction
	ALTER TABLE nfl_boxscore_kicking  
	RENAME COLUMN box_score_id TO boxscore_href;

	alter table nfl_boxscore_kicking
	add column player_id text,
	add column boxscore_id text;

	update nfl_boxscore_kicking 
	set 
	player_id = replace(
		replace(
			SUBSTRING(replace(player_href,'/players/','') FROM POSITION('/' IN replace(player_href,'/players/',''))) 
		,'/','')
	,'.htm',''),
	
	boxscore_id=replace(replace(boxscore_href,'/boxscores/',''),'.htm','');

rollback
--commit
### block ends here ###


## NFL Boxscore offense block
begin transaction
	ALTER TABLE nfl_boxscore_offense  
	RENAME COLUMN box_score_id TO boxscore_href;

	alter table nfl_boxscore_offense
	add column player_id text,
	add column boxscore_id text;

	update nfl_boxscore_offense 
	set 
	player_id = replace(
		replace(
			SUBSTRING(replace(player_href,'/players/','') FROM POSITION('/' IN replace(player_href,'/players/',''))) 
		,'/','')
	,'.htm',''),
	
	boxscore_id=replace(replace(boxscore_href,'/boxscores/',''),'.htm','');

rollback
--commit
### block ends here ###


## NFL Boxscore play byy play block
begin transaction
	ALTER TABLE nfl_boxscore_pbp  
	RENAME COLUMN box_score_id TO boxscore_href;

	alter table nfl_boxscore_pbp
	add column boxscore_id text;

	update nfl_boxscore_pbp 
	set 	
	boxscore_id=replace(replace(boxscore_href,'/boxscores/',''),'.htm','');

rollback
--commit
### block ends here ###


## NFL Boxscore snapcount block
begin transaction
	ALTER TABLE nfl_boxscore_snapcount  
	RENAME COLUMN box_score_id TO boxscore_href;

	alter table nfl_boxscore_snapcount
	add column player_id text,
	add column boxscore_id text;

	update nfl_boxscore_snapcount 
	set 
	player_id = replace(
		replace(
			SUBSTRING(replace(player_href,'/players/','') FROM POSITION('/' IN replace(player_href,'/players/',''))) 
		,'/','')
	,'.htm',''),
	
	boxscore_id=replace(replace(boxscore_href,'/boxscores/',''),'.htm','');

rollback
--commit
### block ends here ###


## NFL Boxscore starters block
begin transaction
	ALTER TABLE nfl_boxscore_starters  
	RENAME COLUMN box_score_id TO boxscore_href;

	alter table nfl_boxscore_starters
	add column player_id text,
	add column boxscore_id text;

	update nfl_boxscore_starters 
	set 
	player_id = replace(
		replace(
			SUBSTRING(replace(player_href,'/players/','') FROM POSITION('/' IN replace(player_href,'/players/',''))) 
		,'/','')
	,'.htm',''),
	
	boxscore_id=replace(replace(boxscore_href,'/boxscores/',''),'.htm','');

rollback
--commit
### block ends here ###


/* Check tables 
select *
from nfl_boxscore_starters nbs 
limit 1000 
*/


