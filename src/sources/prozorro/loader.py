import asyncio
import logging

import httpx


START_URL = 'TODO'


logger = logging.getLogger(__name__)


async def worker(queue, db, session):
    while True:
        page_url = await queue.get()



async def main(args, loglevel=logging.INFO):
    logging.basicConfig(level=log_level)
    
    queue = asyncio.Queue();
    queue.put_nowait(START_URL)
    with create_pool() as pool:
        with httx.AsyncClient() as session:
            workers = [worker(queue, pool, session)
                       for _ in range(args.num_workers)]
            asyncio.gather(*workers)


if __name__ == '__main__':
    from argparse import ArgumentParser
    
    
    parser = ArgumentParser()
    args = parser.parse_args()
    asyncio.run(main())
