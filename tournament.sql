-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

create table players(name text, player_id  serial primary key);
create table matchsrecord(player_id int primary key , points int);
create table numplayed(player_id int primary key, mplayed int);



select players.name,players.player_id,matchsrecord.points,numplayed.mplayed from players left join matchsrecord on players.player_id=matchsrecord.player_id left join numplayed on matchsrecord.player_id=numplayed.player_id;