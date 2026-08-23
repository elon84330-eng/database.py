Skip to content
elon84330-eng
database.py
Repository navigation
Code
Issues
Pull requests
Agents
Actions
Projects
Wiki
Security and quality
database.py
/README.md
Go to file
t
T
elon84330-eng
elon84330-eng
Implement database connection and user registration
70fb95e
 · 
now

Preview

Code

Blame
69 lines (57 loc) · 1.88 KB
import os from datetime import datetime, timezone

import psycopg

def get_connection(): database_url = os.getenv("DATABASE_URL")

if not database_url:
    raise RuntimeError("DATABASE_URL is not configured.")

return psycopg.connect(database_url)
def init_database(): with get_connection() as connection: with connection.cursor() as cursor: cursor.execute( """ CREATE TABLE IF NOT EXISTS users ( id BIGSERIAL PRIMARY KEY, telegram_id BIGINT UNIQUE NOT NULL, username TEXT, first_name TEXT, last_name TEXT, created_at TIMESTAMPTZ NOT NULL, last_seen TIMESTAMPTZ NOT NULL ) """ )

    connection.commit()
def register_user(user): now = datetime.now(timezone.utc)

with get_connection() as connection:
    with connection.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO users (
                telegram_id,
                username,
                first_name,
                last_name,
                created_at,
                last_seen
            )
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (telegram_id)
            DO UPDATE SET
                username = EXCLUDED.username,
                first_name = EXCLUDED.first_name,
                last_name = EXCLUDED.last_name,
                last_seen = EXCLUDED.last_seen
            """,
            (
                user.id,
                user.username,
                user.first_name,
                user.last_name,
                now,
                now,
            ),
        )

    connection.commit()
