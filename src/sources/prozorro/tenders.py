import asyncio
import json
import logging
import os

import aiosql
import asyncpg
import httpx

from sources.prozorro import get, INGESTION_SRC
from utils.db import get_connection, QUERIES


logger = logging.getLogger(__name__)


async def tenders(session, **params):
    "Iterate pages of tenders forward with optional filtering parameters"
    while True:
        result = await get(session, 'tenders', **params)
        yield (e['id'] for e in result['data'])
        if next_page := result.get('next_page'):
            params['offset'] = next_page['offset']
        else:
            break


async def tender(session, tender_id, ocds=True):
    "Get a specific tender by ID. Requests OCDS format by default"
    params = dict(opt_schema='ocds') if ocds else {}
    return await get(session, f'tenders/{tender_id}', **params)


async def ingest_tender(session, conn, tid):
    tender_data = await tender(session, tid)
    logger.info('Ingesting tender %s', tid)
    await QUERIES.insert_doc(conn, src=INGESTION_SRC, doc_id=tid, doc=tender_data)


async def backward_ingest_tenders(session, args):
    "Ingesting tenders backwards, from newer to older. Stop, when there is nothing to ingest for 5 pages."
    pages_completely_ingested = 0
    page_count = 0

    async with get_connection() as conn:
        async for page in tenders(session, descending=1):
            page_ids = set(page)

            # skip already ingested
            ingested = {x['doc_id'] async for x in
                        QUERIES.list_ids_exist(conn, src=INGESTION_SRC, ids=page_ids)}
            logger.info('Already ingested: %d', len(ingested))
            to_ingest = page_ids - ingested

            if args.max_completed_pages > 0 and pages_completely_ingested >= args.max_completed_pages:
                break

            if not to_ingest:
                pages_completely_ingested += 1
                continue

            for tid in to_ingest:
                await ingest_tender(session, conn, tid)

            # TODO: connection pool needed - multiple coros cannot share a single connection
            # asyncio.as_completed(ingest_tender(session, conn, tid)
            #                      for tid in to_ingest)
            page_count += 1

            if args.pages > 0 and page_count >= args.pages:
                logging.info('Ingestion limit reached.')
                break

# async def forward_ingest_tenders


async def main(args):
    async with httpx.AsyncClient(http2=True) as session:
        await backward_ingest_tenders(session, args)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    from argparse import ArgumentParser
    parser = ArgumentParser('Ingesting tender data into DB')
    parser.add_argument('--pages', type=int, default=0, help='Number of pages of tenders to ingest')
    parser.add_argument('--max-completed-pages', type=int, default=0, help='Number of pages of tenders to ingest')
    args = parser.parse_args()
    

    asyncio.run(main(args))
