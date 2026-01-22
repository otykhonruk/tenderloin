import aiosql
import asyncpg
import json
import os
from contextlib import asynccontextmanager


QUERIES = aiosql.from_path('sql/queries', 'asyncpg', mandatory_parameters=False)


@asynccontextmanager
async def get_connection(host='localhost'):
    dsn = 'postgres://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{host}/{POSTGRES_DB}'
    conn = await asyncpg.connect(dsn.format(**os.environ | {'host': host}))
    try:
        await conn.set_type_codec(
            'jsonb',
            encoder=json.dumps,
            decoder=json.loads,
            schema='pg_catalog'
        )
        yield conn
    finally:
        await conn.close()
