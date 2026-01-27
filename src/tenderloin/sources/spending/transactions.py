import asyncio
import logging
from datetime import datetime, timedelta
from operator import itemgetter
from pprint import pprint
from urllib.parse import urljoin

import aiosql
import httpx

from sources.spending import BASE_URL
from utils.db import get_connection, QUERIES

# Test client for spending.gov.ua API endpoints. See:
# https://confluence-ext.spending.gov.ua/spaces/ds/pages/360614/API+Трансакції


PING = 'ping'
LASTLOAD = 'lastload'

logger = logging.getLogger(__name__)


async def ping(session, _):
    "Service availability check"
    response = await session.get(urljoin(BASE_URL, PING))
    return response.status_code


# data.sort(key=itemgetter('lastLoad'), reverse=True)
async def lastload(session, _):
    "Get last loaded date from all sources"
    response = await session.get(urljoin(BASE_URL, LASTLOAD))
    respose.raise_for_status()
    return response.json()


async def transactions(session, params):
    "Get transactions with optional filtering parameters"
    response = await session.get(BASE_URL, params=params)
    response.raise_for_status()
    return response.json()


async def transactions_on_date(session, date):
    "Get transactions for a specific date."
    date_ymd = date.strftime('%Y-%m-%d')
    params = {
        'startdate': date_ymd,
        'enddate': date_ymd
    }
    response = await transactions(session, params)
    return response


async def transactions_by_payer(session, edrpou, end_date=None):
    "Get transactions for a specific EDRPOU code."
    
    if end_date is None:
        end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=90)

    params = {
        'payers_edrpous': edrpou,
        'startdate': start_date.strftime('%Y-%m-%d'),
        'enddate': end_date.strftime('%Y-%m-%d')
    }

    response = await transactions(session, params)
    return response


async def transactions_by_recipient(session, edrpou, end_date=None):
    "Get transactions for a specific EDRPOU code."
    if end_date is None:
        end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=90)

    params = {
        'recipt_edrpous': edrpou,
        'startdate': start_date.strftime('%Y-%m-%d'),
        'enddate': end_date.strftime('%Y-%m-%d')
    }

    response = await transactions(session, params)
    return response


async def test_insert_transaction(db, transaction):
    "Look for transaction, if not found, get, ingest into the database."
    async with get_connection() as conn:
        await QUERIES.spending.insert_transaction(conn, **transaction)


async def main(args):

    async with httpx.AsyncClient(http2=True) as session:
        coro = args.func

        args_dict = vars(args)
        del args_dict['func']

        result = await coro(session, args_dict)
        pprint(result)


if __name__ == '__main__':
    from argparse import ArgumentParser

    logging.basicConfig(level=logging.INFO)
    
    parser = ArgumentParser(description='Spending.gov.ua API Client')
    subparsers = parser.add_subparsers()

    ping_parser = subparsers.add_parser('ping', help='Check service availability')
    ping_parser.set_defaults(func=ping)

    lastload_parser = subparsers.add_parser('lastload', help='Get last loaded data')
    lastload_parser.set_defaults(func=lastload)

    transactions_parser = subparsers.add_parser('transactions', help='Get transactions')
    transactions_parser.add_argument('-s', '--startdate', help='Start date in the yyyy-mm-dd format')
    transactions_parser.add_argument('-e', '--enddate', help='End date in the yyyy-mm-dd format')
    transactions_parser.add_argument('-p', '--payer', help='Comma-separated list of payer EDRPOU codes')
    transactions_parser.add_argument('-r', '--recipient', help='Comma-separated list of recipient EDRPOU codes')
    transactions_parser.set_defaults(func=transactions)
    args = parser.parse_args()

    asyncio.run(main(args))
