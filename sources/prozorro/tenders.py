import asyncio
import json
import os
from urllib.parse import urljoin

import asyncpg
import httpx

from sources.prozorro import get
from utils.db import get_connection


GET_DOC_BY_EDRPOU_QUERY = '''
 SELECT doc FROM ingestion_log WHERE src=$1 and doc->>\'UA-EDR\'=$2
'''

# ЄДРПОУ
# select doc->'procuringEntity'->'identifier'->>'id' from ingestion_log


async def tenders(session, **params):
    "Get tenders with optional filtering parameters"
    response = await get(session, urljoin(URL, 'tenders'), params=params)


async def tender(session, tender_id):
    "Get a specific tender by ID"
    path = f'tenders/{tender_id}'
    return await get(session, urljoin(URL, path))


async def main(args):
    async with httpx.AsyncClient(http2=True) as session:
        result = await tenders(session, descending=1)
        async with get_connection() as db_conn:
            for t in result:
                await ingest_tender(session, db_conn, t['id'])


if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-t', '--tender')
    args = parser.parse_args()

    asyncio.run(main(args))
