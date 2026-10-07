-- Sample data for LeagueDB. Run the schema script first
INSERT INTO teams (team_id,team_name,city)
VALUES
     (1,'River Hawks','Riverside'),
     (2,'Mountain Lions','Highland'),
     (3,'Valley Vipers','Sunnyvale');
INSERT INTO players (player_id,player_name,team_id,goals)
VALUES
     (1,'Ana Torres',1,5),
     (2,'Ben Okafor',1,3),
     (3,'Carla Mendes',2,4),
     (4,'Dev Patel',2,6),
     (5,'Eli Novak',3,2);
-- Results: Hawks win, draw,Hawks win, draw,Vipers win.
INSERT INTO matches (match_id,home_team_id,away_team_id,home_goals,away_goals)
VALUES
     (1,1,2,3,1),
     (2,2,3,2,2),
     (3,1,3,4,0),
     (4,3,2,1,1),
     (5,2,1,0,2);