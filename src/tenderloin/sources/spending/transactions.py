import asyncio
import logging
from datetime import datetime, timedelta, date
from operator import itemgetter
from pprint import pprint

import aiosql
import httpx

from tenderloin.sources.spending import get
from tenderloin.utils.db import get_connection, QUERIES


# Test client for spending.gov.ua API endpoints. See:
# https://confluence-ext.spending.gov.ua/spaces/ds/pages/360614/API+Трансакції


PING = 'transactions/ping'
LASTLOAD = 'transactions/lastload'
TRANSACTIONS = 'transactions/'

logger = logging.getLogger(__name__)


async def ping(session, _):
    "Service availability check"
    response = await get(session, PING)
    return response.status_code


async def lastload(session, _):
    "Get last loaded date from all sources"
    response = await get(session, LASTLOAD)
    data = response.json()
    data.sort(key=itemgetter('lastLoad'), reverse=True)
    return data

async def transactions(session, params):
    "Get transactions with optional filtering parameters"
    response = await get(session, TRANSACTIONS, params=params)
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


async def test_insert_transactions(session, params):
    "Look for transaction, if not found, get, ingest into the database."
    data = await transactions_on_date(session, date(2026,1,27))
    async with get_connection() as conn:
        for transaction in data:
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
    transactions_parser.set_defaults(func=test_insert_transactions)
    args = parser.parse_args()

    asyncio.run(main(args))
