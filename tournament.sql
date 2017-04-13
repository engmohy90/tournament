-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.
DROP DATABASE tournament; 
CREATE DATABASE tournament;
\c tournament

create table players(
		name text,
		player_id  serial primary key,
		points int default 0,
		match_played int default 0
);
