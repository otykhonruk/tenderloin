INGESTION_SRC = 'prz'
BASE_URL = 'https://public-api.prozorro.gov.ua/api/2.5/'


async def get(session, path, **params):
    "Generic GET request to the Prozorro API"
    response = await session.get(urljoin(URL, path), params=params)
    response.raise_for_status()
    return response.json()['data']
