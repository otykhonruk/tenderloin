import logging
from urllib.parse import urljoin

from httpx import TimeoutException


BASE_URL = 'https://api.spending.gov.ua/api/v2/api/'
SWAGGER_URL  = 'https://api.spending.gov.ua/api/swagger-ui.html'
USER_AGENT = 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.2 Safari/605.1.15'


logger = logging.getLogger(__name__)


async def get(session, path, **kwargs):
    try:
        response = await session.get(urljoin(BASE_URL, path), **kwargs)
        response.raise_for_status()
        return response
    except TimeoutException as e:
        logger.exception('Timeout for spending.gov.ua, will try to wake it up by requesting static page from a "browser".')
        try:
            await session.get(SWAGGER_URL, headers={'user-agent': USER_AGENT})
        except:
            pass
        # second try
        response = await session.get(urljoin(BASE_URL, path), **kwargs)
        response.raise_for_status()
        return response
