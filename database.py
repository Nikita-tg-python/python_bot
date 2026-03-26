import os
import asyncpg
from datetime import datetime

pool = None


async def create_pool():
    global pool
    pool = await asyncpg.create_pool(
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        ssl="require",
    )


async def create_table():
    async with pool.acquire() as connection:
        await connection.execute(
            """
            CREATE TABLE IF NOT EXISTS visitors_log (
                user_id BIGINT PRIMARY KEY,
                first_name TEXT,
                username TEXT,
                last_action TEXT,
                last_visit TIMESTAMP
            )
        """
        )


async def log_user_action(user_id: int, first_name: str, username: str, action: str):
    async with pool.acquire() as connection:
        now = datetime.now()

        await connection.execute(
            """
            INSERT INTO visitors_log (user_id, first_name, username, last_action, last_visit)
            VALUES ($1, $2, $3, $4, $5)
            ON CONFLICT (user_id) DO UPDATE
            SET last_action = EXCLUDED.last_action,
                last_visit = EXCLUDED.last_visit,
                first_name = EXCLUDED.first_name,
                username = EXCLUDED.username
        """,
            user_id,
            first_name,
            username,
            action,
            now,
        )
