"""Build LeagueDB from the SQL scripts and print what every query returns.

The SQL files are the project; this script only runs them the same way
DBeaver's "Execute SQL Script" does, one statement at a time.
"""
import os
import sqlite3
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SQL_DIR = os.path.join(HERE, "sql")
DB_PATH = os.path.join(HERE, "LeagueDB.db")


def read_sql(name):
    # utf-8-sig drops a byte-order mark if an editor saved one.
    with open(os.path.join(SQL_DIR, name), encoding="utf-8-sig") as f:
        return f.read()


def split_statements(text):
    """Cut a script into single statements, keeping the comments above each one."""
    statements = []
    current = ""
    for line in text.splitlines():
        current += line + "\n"
        # complete_statement ignores semicolons inside quotes and comments.
        if sqlite3.complete_statement(current):
            statements.append(current.strip())
            current = ""
    leftover = [l for l in current.splitlines() if l.strip() and not l.strip().startswith("--")]
    if leftover:
        raise ValueError("statement without a closing semicolon: " + " ".join(leftover))
    return statements


def run_script(conn, name):
    """Run every statement in one SQL file. Returns (statement, columns, rows) for each."""
    results = []
    for statement in split_statements(read_sql(name)):
        cursor = conn.execute(statement)
        if cursor.description:
            columns = [d[0] for d in cursor.description]
            results.append((statement, columns, cursor.fetchall()))
        else:
            results.append((statement, None, cursor.rowcount))
    conn.commit()
    return results


def build(conn):
    run_script(conn, "schema.sql")
    run_script(conn, "seed.sql")


def format_table(columns, rows):
    cells = [columns] + [["NULL" if v is None else str(v) for v in row] for row in rows]
    widths = [max(len(r[i]) for r in cells) for i in range(len(columns))]
    lines = [" | ".join(c.ljust(w) for c, w in zip(r, widths)).rstrip() for r in cells]
    lines.insert(1, "-+-".join("-" * w for w in widths))
    return "\n".join(lines)


def heading(statement):
    """First line of the comment block written just above the statement."""
    title = None
    previous_was_comment = False
    for line in statement.splitlines():
        is_comment = line.strip().startswith("--")
        if is_comment and not previous_was_comment:
            title = line.strip()[2:].strip()
        previous_was_comment = is_comment
    return title or statement.splitlines()[0]


def main():
    conn = sqlite3.connect(DB_PATH)
    try:
        build(conn)
        for statement, columns, result in run_script(conn, "queries.sql"):
            print("== " + heading(statement))
            if columns is None:
                print(f"{result} row(s) changed")
            else:
                print(format_table(columns, result))
            print()
    finally:
        conn.close()
    print("LeagueDB.db is ready to open in DBeaver.")
    return 0


if __name__ == "__main__":
    sys.exit(main())