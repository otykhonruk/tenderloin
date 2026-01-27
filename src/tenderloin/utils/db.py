import aiosql
import asyncpg
import json
import os
from contextlib import asynccontextmanager


DSN = 'postgres://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{host}/{POSTGRES_DB}'
QUERIES = aiosql.from_path('sql/queries', 'asyncpg', mandatory_parameters=False)


async def set_connection_codecs(conn):
    await conn.set_type_codec('jsonb',
                              schema='pg_catalog',
                              encoder=json.dumps,
                              decoder=json.loads)


# https://magicstack.github.io/asyncpg/current/usage.html#connection-pools
@asynccontextmanager
async def create_pool(host='localhost'):
    "Returns configured connection pool"
    pool = await asyncpg.create_pool(
        dsn=DSN.format(**os.environ | {'host': host}),
        init=set_connection_codecs)
    yield pool
    await pool.close()


@asynccontextmanager
async def get_connection(host='localhost'):
    conn = await asyncpg.connect(
        dsn=DSN.format(**os.environ | {'host': host}))
    try:
        await set_connection_codecs(conn)
        yield conn
    finally:
        await conn.close()
