import asyncio

from tinkoff.invest import AsyncClient, GetAccountsResponse, PortfolioResponse
from tinkoff.invest.async_services import AsyncServices


class TinkoffClientService:
    """
    Wrapper for tinkoff.invest.AsyncClient.
    Takes responsibility for choosing correct function to call basing on
    sandbox mode flag.
    """

    def __init__(self, token: str, sandbox: bool = True):
        self.token = token
        self.sandbox = sandbox
        self.client: AsyncClient
        self.servicies: AsyncServices

    async def __aenter__(self):
        self.client = AsyncClient(token=self.token, app_name="tracfolio")
        self.servicies = await self.client.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        return await self.client.__aexit__(exc_type, exc_val, exc_tb)

    async def get_accounts(self) -> GetAccountsResponse:
        if self.sandbox:
            sandbox_accounts = await self.servicies.sandbox.get_sandbox_accounts()
            if len(sandbox_accounts.accounts) == 0:
                await self.servicies.sandbox.open_sandbox_account()
                await asyncio.sleep(3)
                await self.get_accounts()
            return sandbox_accounts
        return await self.servicies.users.get_accounts()

    async def get_portfolio(self, account_id: str, **kwargs) -> PortfolioResponse:
        if self.sandbox:
            return await self.servicies.sandbox.get_sandbox_portfolio(
                account_id=account_id, **kwargs
            )
        return await self.servicies.operations.get_portfolio(
            account_id=account_id, **kwargs
        )
