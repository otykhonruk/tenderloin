import asyncio
from urllib.parse import urljoin

import httpx

# Test client for dream.gov.ua API endpoints.
# Description:
# https://docs.google.com/document/d/1ncXkBgLt5lT7nUUWPIYOaMwadDgQ_hcNYKi3nbXj1cM/edit#heading=h.hs6dr9ypa5n1
# Swagger:
# https://open-contracting.github.io/dream-api-docs/


BASE_URL="https://public-api.dream.gov.ua/marketplace/public/dream/"

IDEAS = 'ideas'


async def ideas(session, **params):
    "Get ideas with optional filtering parameters"
    response = await session.get(urljoin(BASE_URL, IDEAS), params=params)
    if response.status_code == 200:
        return response.json()['data']


async def idea(session, idea_id):
    "Get a specific idea by ID"
    response = await session.get(f"{BASE_URL}{IDEAS}/{idea_id}")
    if response.status_code == 200:
        return response.json()
    else:
        print(f'Idea id: {idea_id}')
        print(response.request.url)
        print(response)


async def main(args):
    from pprint import pprint
    async with httpx.AsyncClient(http2=True) as session:
        result = await ideas(session, order='desc')
        id_ = result[0]['internal']['id']
        idea_data = await idea(session, id_)
        pprint(idea_data)


if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-i', '--idea')
    args = parser.parse_args()
    asyncio.run(main(args))
    
    
