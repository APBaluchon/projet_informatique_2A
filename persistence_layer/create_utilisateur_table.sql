-- Title: utilisateur.sql
-- Project: GameGenius
-- Description: SQL script to create the utilisateur table
CREATE TABLE utilisateur (
	pseudo varchar NOT NULL,
	mdp varchar NULL,
	"role" varchar NULL
);
ALTER TABLE utilisateur ADD PRIMARY KEY (pseudo);

INSERT INTO utilisateur (pseudo, mdp, "role") VALUES ('admin', '123', 'admin');