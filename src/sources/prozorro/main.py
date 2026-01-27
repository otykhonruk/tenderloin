from typing import Any
from aiohttp import ClientSession
from prozorro_crawler.main import main as run_crawler


async def item_data_handler(session: ClientSession, items: list[dict[str, Any]]) -> None:
    for item in items:
        print(f"Item with id {item['id']} and status {item['status']} got updated!")

if __name__ == "__main__":
    run_crawler(  # this will run IO loop and process feed updates
        data_handler=item_data_handler,
        opt_fields=["status"],
        resource="tenders",  # can be plans, contracts, frameworks, etc.
    )
