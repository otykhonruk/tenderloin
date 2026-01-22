from urllib.parse import urljoin

INGESTION_SRC = 'P'
BASE_URL = 'https://public-api.prozorro.gov.ua/api/2.5/'


async def get(session, path, **params):
    "Generic GET request to the Prozorro API"
    response = await session.get(urljoin(BASE_URL, path), params=params)
    response.raise_for_status()
    return response.json()['data']
