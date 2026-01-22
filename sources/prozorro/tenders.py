import asyncio
import json
import os

import aiosql
import asyncpg
import httpx

from sources.prozorro import get, INGESTION_SRC
from utils.db import get_connection, QUERIES


async def tenders(session, **params):
    "Iterate pages of tenders with optional filtering parameters"
    next_page = True
    while next_page:
        result = await get(session, 'tenders', **params)
        yield (e['id'] for e in result['data'])
        if next_page := result.get('next_page'):
            params['offset'] = next_page['offset']


async def tender(session, tender_id):
    "Get a specific tender by ID"
    return await get(session, f'tenders/{tender_id}')


async def ingest_tenders(session, args):
    pages = 0
    async with get_connection() as conn:
        async for page in tenders(session, descending=1):
            if pages >= args.test_ingest:
                break

            for tid in page:
                tender_data = await tender(session, tid)
                print('Ingesting tender', tid)
                await QUERIES.insert_doc(conn, src=INGESTION_SRC, doc_id=tid, doc=tender_data)

            pages += 1


async def main(args):
    # test ingestion
    async with httpx.AsyncClient(http2=True) as session:
        if args.test_ingest:
            await ingest_tenders(session, args)



if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('--test-ingest', type=int, default=0, help='Number of pages of tenders to ingest')
    args = parser.parse_args()
    

    asyncio.run(main(args))
