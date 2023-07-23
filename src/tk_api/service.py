import asyncio

from tinkoff.invest import AsyncClient

from src.config import settings

TOKEN = settings.invest_token


async def main():
    async with AsyncClient(TOKEN) as client:
        accounts = await client.users.get_accounts()
        accounts.accounts
        print(await client.users.get_accounts())

if __name__ == "__main__":
    asyncio.run(main())
