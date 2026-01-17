import asyncio
from operator import itemgetter
from urllib.parse import urljoin

import httpx

# Test client for spending.gov.ua API endpoints. See:
# https://confluence-ext.spending.gov.ua/spaces/ds/pages/360614/API+Трансакції

BASE_URL = 'https://api.spending.gov.ua/api/v2/api/transactions'

PING = 'ping'
LASTLOAD = 'lastload'


async def ping(session):
    "Service availability check"
    async with session.get(urljoin(BASE_URL, PING)) as response:
        return response.status


async def lastload(session):
    "Get last loaded date from all sources"
    async with session.get(urljoin(BASE_URL, LASTLOAD)) as response:
        return await response.json()


async def transactions(session, params=None):
    "Get transactions with optional filtering parameters"
    async with session.get(BASE_URL, params=params) as response:
        return await response.json()


async def main():
    async with httpx.Client() as session:
        status = await ping(session)
        print(f'Ping status: {status}')
        print('\nLast loaded data (top 10):')

        data = await lastload(session)
        data.sort(key=itemgetter('lastLoad'), reverse=True)
        
        for rec in data[:10]:
            print("{lastLoad}\t{sourceName}".format(**rec))


if __name__ == '__main__':
    import asyncio
    
    asyncio.run(main())
