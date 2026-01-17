import asyncio
from urllib.parse import urljoin

import httpx


URL = 'https://public-api.prozorro.gov.ua/api/2.5/'


async def tenders(session, **params):
    "Get tenders with optional filtering parameters"
    response = await session.get(urljoin(URL, 'tenders'), params=params)
    if response.status_code == httpx.codes.OK:
        return response.json()['data']


async def tender(session, tender_id):
    "Get a specific tender by ID"
    response = await session.get(urljoin(URL, 'tenders/' + tender_id))
    if response.status_code == httpx.codes.OK:
        return response.json()
    else:
        print(f'Tender id: {tender_id}')
        print(response.request.url)
        print(response)


async def main(args):
        from pprint import pprint

        async with httpx.AsyncClient(http2=True) as session:
            # result = await tenders(session, descending=1)
            
            result = await tender(session, args.tender)
            pprint(result)


if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-t', '--tender')
    args = parser.parse_args()

    asyncio.run(main(args))
