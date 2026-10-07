-- League standings

WITH team_matches AS (
    SELECT
        t.team_id,
        t.team_name,
        m.match_id,
        m.home_goals AS goals_for,
        m.away_goals AS goals_against
    FROM teams t
    JOIN matches m
        ON t.team_id = m.home_team_id

    UNION ALL

    SELECT
        t.team_id,
        t.team_name,
        m.match_id,
        m.away_goals AS goals_for,
        m.home_goals AS goals_against
    FROM teams t
    JOIN matches m
        ON t.team_id = m.away_team_id
)

SELECT
    team_id,
    team_name,
    COUNT(match_id) AS played,
    SUM(CASE WHEN goals_for > goals_against THEN 1 ELSE 0 END) AS wins,
    SUM(CASE WHEN goals_for = goals_against THEN 1 ELSE 0 END) AS draws,
    SUM(CASE WHEN goals_for < goals_against THEN 1 ELSE 0 END) AS losses,
    SUM(
        CASE
            WHEN goals_for > goals_against THEN 3
            WHEN goals_for = goals_against THEN 1
            ELSE 0
        END
    ) AS points
FROM team_matches
GROUP BY team_id, team_name
ORDER BY points DESC, team_id;


-- Top scorer

SELECT
    player_id,
    player_name,
    team_id,
    goals
FROM players
ORDER BY goals DESC, player_id
LIMIT 1;