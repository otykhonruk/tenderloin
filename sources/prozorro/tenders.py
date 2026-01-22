import asyncio
import json
import os

import aiosql
import asyncpg
import httpx

from sources.prozorro import get, INGESTION_SRC
from utils.db import get_connection


queries = aiosql.from_path('sql/queries', 'asyncpg', mandatory_parameters=False)


async def tenders(session, **params):
    "Get tenders with optional filtering parameters"
    return await get(session, 'tenders', params=params)


async def tender(session, tender_id):
    "Get a specific tender by ID"
    return await get(session, f'tenders/{tender_id}')


async def main(args):
    # test ingestion
    async with httpx.AsyncClient(http2=True) as session:
        result = await tenders(session, descending=1)
        async with get_connection() as conn:
            for r in result:
                tid = r['id']
                tender_data = await tender(session, tid)
                print('Ingesting tender', tid)
                await queries.ingest_doc(conn, src=INGESTION_SRC, doc_id=tid, doc=tender_data)


if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    args = parser.parse_args()

    asyncio.run(main(args))
