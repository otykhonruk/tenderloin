import asyncio
import os
import json
from pprint import pprint

import aiosql
import asyncpg

from utils import display_dict
from utils.db import get_connection, QUERIES


async def get_doc(src, doc_id):
    "Get document from database by source and ID"
    async with get_connection() as conn:
        return await QUERIES.get_doc_by_id(conn, src=src, id=doc_id)


async def export_doc(src, doc_id):
    "Export document from database into human-readable JSON file"
    doc = await get_doc(src, doc_id)
    with open(f'{src}_{doc_id}.json', 'w', encoding='utf-8') as f:
        json.dump(doc, f, ensure_ascii=False, indent=2)

        
async def export(args):
    if args.doc_id:
        await export_doc(args.src, args.doc_id)
    else:
        async for doc_id in list_ids(args.src):
            await export_doc(args.src, doc_id)


async def list_ids(src):
    "List document IDs by source"
    async with get_connection() as conn:
        async for r in QUERIES.list_ids(conn, src=src):
            yield r['doc_id']


async def list_by_src(args):
    async for id_ in list_ids(args.src):
        print(id_)

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
    list_docs.set_defaults(func=list_by_src)

    docs_parser = subparsers.add_parser('doc', help='Get document by source and ID')
    docs_parser.add_argument('doc_id', help='Document ID')
    docs_parser.set_defaults(func=get_doc)

    export_parser = subparsers.add_parser('export', help='Export document to JSON file')
    export_parser.add_argument('-d', '--doc_id', help='Document ID', required=False)
    export_parser.set_defaults(func=export)

    args = parser.parse_args()

    asyncio.run(main(args))
