#!/bin/bash

postgres_ready() {
python << END
import asyncio
import asyncpg
import sys

async def check_postgres():
    try:
        conn = await asyncpg.connect(
            database="${POSTGRES_DB}",
            user="${POSTGRES_USER}",
            password="${POSTGRES_PASSWORD}",
            host="${POSTGRES_HOST}",
            port="${POSTGRES_PORT}",
        )
        await conn.close()
        return True
    except asyncpg.exceptions.PostgresError:
        return False

async def main():
    if await check_postgres():
        sys.exit(0)
    else:
        sys.exit(-1)

asyncio.run(main())
END
}
until postgres_ready; do
  >&2 echo 'Waiting for PostgreSQL to become available...'
  sleep 1
done
>&2 echo 'PostgreSQL is available'

alembic upgrade head

uvicorn main:app --host 0.0.0.0 --port 8000
