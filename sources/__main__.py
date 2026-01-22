import asyncio
import os
import json
from pprint import pprint

import aiosql
import asyncpg

from utils import display_dict
from utils.db import get_connection, QUERIES


async def get_doc(args):
    "Get document from database by source and ID"
    async with get_connection() as conn:
        return await QUERIES.get_doc_by_id(conn, src=args.src, id=args.doc_id)


async def export_doc(args):
    "Export document from database into human-readable JSON file"
    doc = await get_doc(args)
    with open(f'{args.src}_{args.doc_id}.json', 'w', encoding='utf-8') as f:
        json.dump(doc, f, ensure_ascii=False, indent=2)


async def list_ids(args):
    "List document IDs by source"
    async with get_connection() as conn:
        async for r in QUERIES.list_ids(conn, src=args.src):
            print(r['doc_id'])


# async def get_doc_by_edrpou():
#    pass


async def main(args):
    res = await args.func(args)
    if res:
        pprint(display_dict(res))


if __name__ == '__main__':
    import asyncio
    from argparse import ArgumentParser

    SOURCES = ['P', 'D']
    
    parser = ArgumentParser(description='')
    parser.add_argument('-s', '--src', help='Source name', choices=SOURCES)
    subparsers = parser.add_subparsers()

    list_docs = subparsers.add_parser('list', help='List document IDs by source')
    list_docs.set_defaults(func=list_ids)

    docs = subparsers.add_parser('doc', help='Get document by source and ID')
    docs.add_argument('doc_id', help='Document ID')
    docs.set_defaults(func=get_doc)

    export = subparsers.add_parser('export', help='Export document to JSON file')
    export.add_argument('doc_id', help='Document ID')
    export.set_defaults(func=export_doc)

    args = parser.parse_args()

    asyncio.run(main(args))
