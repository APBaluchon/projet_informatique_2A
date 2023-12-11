-- Title: utilisateur.sql
-- Project: GameGenius
-- Description: SQL script to create the utilisateur table
CREATE TABLE utilisateur (
	pseudo varchar NOT NULL,
	mdp varchar NULL,
	"role" varchar NULL
);
ALTER TABLE utilisateur ADD PRIMARY KEY (pseudo);

INSERT INTO utilisateur (pseudo, mdp, "role") VALUES ('admin', '4fc82b26aecb47d2868c4efbe3581732a3e7cbcc6c2efb32062c08170a05eeb8', 'admin');