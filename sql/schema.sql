-- LeagueDB: the three tables of the community sports league.
-- Dropping first means you can run this script again and start clean.
-- Children (players, matches) are dropped before the parent (teams).

DROP TABLE IF EXISTS matches;
DROP TABLE IF EXISTS players;
DROP TABLE IF EXISTS teams;

CREATE TABLE teams (
    team_id   INTEGER PRIMARY KEY,
    team_name TEXT,
    city      TEXT
);

CREATE TABLE players (
    player_id   INTEGER PRIMARY KEY,
    player_name TEXT,
    team_id     INTEGER,
    goals       INTEGER
);

CREATE TABLE matches (
    match_id     INTEGER PRIMARY KEY,
    home_team_id INTEGER,
    away_team_id INTEGER,
    home_goals   INTEGER,
    away_goals   INTEGER
);