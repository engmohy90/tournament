-- Table definitions for the tournament project.
--
-- Put your SQL 'CREATE TABLE' statements in this file; also 'CREATE view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.
DROP DATABASE tournament; 
CREATE DATABASE tournament;
\c tournament

CREATE TABLE players(
        name text,
        player_id  serial primary key
);
CREATE TABLE record(
        points int,
        player_id  int primary key
);
CREATE TABLE match(
        match_played int,
        player_id  int primary key
);
CREATE VIEW all_record AS
    SELECT 
        player_id,
        name,
        (SELECT count(points) FROM record WHERE
         players.player_id=record.player_id) AS wins,
        (SELECT count(match_played) FROM match WHERE
         players.player_id=match.player_id) AS played
    FROM players 
    ORDER BY wins;
