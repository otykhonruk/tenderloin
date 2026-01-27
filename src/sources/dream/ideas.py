import asyncio
import json
import logging
import os
from urllib.parse import urljoin

import aiosql
import asyncpg
import httpx

from sources.dream import BASE_URL
from utils.db import get_connection, QUERIES


# Test client for dream.gov.ua API endpoints.
#
# Description:
# https://docs.google.com/document/d/1ncXkBgLt5lT7nUUWPIYOaMwadDgQ_hcNYKi3nbXj1cM/edit#heading=h.hs6dr9ypa5n1
#
# Swagger:
# https://open-contracting.github.io/dream-api-docs/


IDEAS = 'ideas'

logger = logging.getLogger(__name__)


async def ideas(session, **params):
    "Get ideas with optional filtering parameters"
    while True:
        response = await session.get(urljoin(BASE_URL, IDEAS), params=params)
        response.raise_for_status()
        data = response.json()['data']
        if data:
            params['from'] = data[-1]['external']['updated']
            yield (idea['internal']['id'] for idea in data)
        else:
            break


async def idea(session, idea_id):
    "Get a specific idea by ID"
    response = await session.get(f"{BASE_URL}{IDEAS}/{idea_id}")
    response.raise_for_status()
    return response.json()


async def backward_ingest_ideas(session, conn, args):
    page_count = 0
    async for page in ideas(session, order='desc'):
        page_ids = set(page)
        ingested = {x['id'] async for x in
                    QUERIES.dream.ideas_exist(conn, ids=page_ids)}
        to_ingest = page_ids - ingested

        if not to_ingest:
            continue

        for id_ in to_ingest:
            idea_data = await idea(session, id_)
            params = idea_data['internal']
            params['cdu_response'] = idea_data['cdu_response']
            logger.info('Ingesting idea ID: %s', id_)
            await QUERIES.dream.ingest_doc(conn, **params)

        page_count += 1
        if args.pages > 0 and page_count >= args.pages:
            logging.info('Ingestion limit reached.')
            break


async def main(args):
    logging.basicConfig(level=logging.INFO)

    async with httpx.AsyncClient(http2=True) as session:
        async with get_connection() as conn:
            await backward_ingest_ideas(session, conn, args)


if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('--pages', type=int, default=0, help='Number of pages of ideas to ingest')
    args = parser.parse_args()
    asyncio.run(main(args))
