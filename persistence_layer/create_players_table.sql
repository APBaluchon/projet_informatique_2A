-- Title: players.sql
-- Project: GameGenius
-- Description: SQL script to create the players table
CREATE TABLE players (
	puuid varchar(100) NOT NULL,
	summonername varchar(50) NOT NULL,
	rang varchar(40) NOT NULL
);
ALTER TABLE players ADD PRIMARY KEY (puuid);