import asyncio
import os
import json
from pprint import pprint

import asyncpg

from utils import display_dict
from utils.db import get_connection


GENERIC_INGEST_DOC_QUERY = '''
 INSERT INTO ingestion_log(status, src, doc_id, doc) VALUES($1, $2, $3, $4) ON CONFLICT DO NOTHING
'''

GET_DOC_BY_ID_QUERY = 'SELECT doc FROM ingestion_log WHERE src=$1 and doc_id=$2'

LIST_DOCS_QUERY = 'SELECT doc_id FROM ingestion_log WHERE src=$1'


async def ingest_doc(db_conn, src, doc_id, data):
    await db_conn.execute(GENERIC_INGEST_DOC_QUERY, 'ok', src, doc_id, data)


async def get_doc(db_conn, args):
    doc = await db_conn.fetchval(GET_DOC_BY_ID_QUERY, args.src, args.doc_id)
    return doc


async def get_doc_by_edrpou():
    pass


async def export_doc(db_conn, args):
    doc = await get_doc(db_conn, args)
    with open(f'{args.src}_{args.doc_id}.json', 'w', encoding='utf-8') as f:
        json.dump(doc, f, ensure_ascii=False, indent=2)


async def list_docs_by_src(db_conn, args):
    return await db_conn.fetch(LIST_DOCS_QUERY, args.src)


async def main(args, coro):
    async with get_connection() as db_conn:
        res = await coro(db_conn, args)
        if res:
            pprint(display_dict(res))
        # doc = await get_doc(db_conn, args.src, args.doc_id)


if __name__ == '__main__':
    import asyncio
    from argparse import ArgumentParser

    parser = ArgumentParser(description='')
    subparsers = parser.add_subparsers()
    list_docs = subparsers.add_parser('list', help='List document IDs by source')
    list_docs.add_argument('-s', '--src', help='Source name', choices=['prz', 'spd', 'drm'])
    list_docs.set_defaults(func=list_docs_by_src)

    docs = subparsers.add_parser('doc', help='Get document by source and ID')
    docs.add_argument('-s', '--src', help='Source name', choices=['prz', 'spd', 'drm'])
    docs.add_argument('-d', '--doc-id', help='Document ID')
    docs.set_defaults(func=get_doc)

    export = subparsers.add_parser('export', help='Export document to JSON file')
    export.add_argument('-s', '--src', help='Source name', choices=['prz', 'spd', 'drm'])
    export.add_argument('-d', '--doc-id', help='Document ID')
    export.set_defaults(func=export_doc)

    args = parser.parse_args()

    asyncio.run(main(args, args.func))
