import asyncio
from operator import itemgetter
from urllib.parse import urljoin

import httpx

from sources.spending import BASE_URL

# Test client for spending.gov.ua API endpoints. See:
# https://confluence-ext.spending.gov.ua/spaces/ds/pages/360614/API+Трансакції


PING = 'ping'
LASTLOAD = 'lastload'


async def ping(session):
    "Service availability check"
    response = await session.get(urljoin(BASE_URL, PING))
    return response.status_code


async def lastload(session):
    "Get last loaded date from all sources"
    response = await session.get(urljoin(BASE_URL, LASTLOAD))
    return await response.json()


async def transactions(session, params=None):
    "Get transactions with optional filtering parameters"
    response = await session.get(BASE_URL, params=params)
    return await response.json()


async def transaction(session, db, id_):
    "Get a specific transaction by database and ID"
    
    url = urljoin(BASE_URL)
    async with session.get(url) as response:
        if response.status_code != httpx.codes.OK:
            response.raise_for_status()
        data = await response.json()


async def main():
    async with httpx.AsyncClient(http2=True) as session:
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
