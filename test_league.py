import sqlite3
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
DB_PATH = ROOT / "LeagueDB.db"


def run_league():
    """Build the database and run the project's SQL queries."""
    result = subprocess.run(
        [sys.executable, str(ROOT / "league.py")],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, (
        "league.py failed:\n"
        + result.stdout
        + "\n"
        + result.stderr
    )


def test_database_created():
    run_league()

    assert DB_PATH.exists(), "LeagueDB.db was not created"


def test_league_standings():
    run_league()

    conn = sqlite3.connect(DB_PATH)

    rows = conn.execute(
        """
        SELECT
            t.team_id,
            t.team_name,
            COUNT(m.match_id) AS played,
            SUM(
                CASE
                    WHEN
                        (m.home_team_id = t.team_id
                         AND m.home_goals > m.away_goals)
                        OR
                        (m.away_team_id = t.team_id
                         AND m.away_goals > m.home_goals)
                    THEN 1
                    ELSE 0
                END
            ) AS wins,
            SUM(
                CASE
                    WHEN m.home_goals = m.away_goals
                    THEN 1
                    ELSE 0
                END
            ) AS draws,
            SUM(
                CASE
                    WHEN
                        (m.home_team_id = t.team_id
                         AND m.home_goals < m.away_goals)
                        OR
                        (m.away_team_id = t.team_id
                         AND m.away_goals < m.home_goals)
                    THEN 1
                    ELSE 0
                END
            ) AS losses,
            SUM(
                CASE
                    WHEN
                        (m.home_team_id = t.team_id
                         AND m.home_goals > m.away_goals)
                        OR
                        (m.away_team_id = t.team_id
                         AND m.away_goals > m.home_goals)
                    THEN 3
                    WHEN m.home_goals = m.away_goals
                    THEN 1
                    ELSE 0
                END
            ) AS points
        FROM teams t
        JOIN matches m
            ON t.team_id = m.home_team_id
            OR t.team_id = m.away_team_id
        GROUP BY t.team_id, t.team_name
        ORDER BY points DESC, t.team_id
        """
    ).fetchall()

    conn.close()

    expected = [
        (1, "River Hawks", 3, 2, 1, 0, 7),
        (2, "Mountain Lions", 4, 0, 2, 2, 2),
        (3, "Valley Vipers", 3, 1, 1, 1, 4),
    ]

    assert rows == expected


def test_top_scorer():
    run_league()

    conn = sqlite3.connect(DB_PATH)

    row = conn.execute(
        """
        SELECT player_id, player_name, team_id, goals
        FROM players
        ORDER BY goals DESC, player_id
        LIMIT 1
        """
    ).fetchone()

    conn.close()

    assert row == (1, "Ana Torres", 1, 7)