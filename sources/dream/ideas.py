import asyncio
import json
import os
from urllib.parse import urljoin

import aiosql
import asyncpg
import httpx

from sources.dream import BASE_URL, INGESTION_SRC
from utils import display_dict
from utils.db import get_connection


# Test client for dream.gov.ua API endpoints.
#
# Description:
#
# https://docs.google.com/document/d/1ncXkBgLt5lT7nUUWPIYOaMwadDgQ_hcNYKi3nbXj1cM/edit#heading=h.hs6dr9ypa5n1
#
# Swagger:
# https://open-contracting.github.io/dream-api-docs/


queries = aiosql.from_path("sql/queries", "asyncpg", mandatory_parameters=False)


IDEAS = 'ideas'


async def ideas(session, **params):
    "Get ideas with optional filtering parameters"
    response = await session.get(urljoin(BASE_URL, IDEAS), params=params)
    response.raise_for_status()
    return response.json()['data']


async def idea(session, idea_id):
    "Get a specific idea by ID"
    response = await session.get(f"{BASE_URL}{IDEAS}/{idea_id}")
    response.raise_for_status()
    return response.json()['cdu_response']


async def main(args):
    # test ingestion

    async with httpx.AsyncClient(http2=True) as session:
        result = await ideas(session, order='desc')
        print(f'Total ideas: {len(result)}')
        ids = [idea['internal']['id'] for idea in result]
        idea_data = await idea(session, ids[0])
        
        # ingest 100 ideas

        async with get_connection() as conn:
            for id_ in ids[:100]:
                idea_data = await idea(session, id_)
                print('Ingesting idea ID:', id_)
                await queries.ingest_doc(conn, src=INGESTION_SRC, doc_id=id_, doc=idea_data)



if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    args = parser.parse_args()
    asyncio.run(main(args))
