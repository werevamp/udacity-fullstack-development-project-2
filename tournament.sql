-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

CREATE DATABASE tournament;

\connect tournament;

DROP TABLE IF EXISTS players CASCADE;
DROP TABLE IF EXISTS player_statistics CASCADE;
DROP TABLE IF EXISTS matches CASCADE;

-- id, name
CREATE TABLE players (name TEXT,
											id SERIAL );

--This table is probably not needed
--player_id, win, lose
CREATE TABLE player_statistics (id smallint,
															 win smallint,
															 lose smallint );

--first_player_id, second_player_id, winner, depth
CREATE TABLE matches (id SERIAL,
											winner smallint,
											loser smallint,
											round smallint );
--you could possible get the winner through player_statistic 

--CREATE TABLE tournaments
