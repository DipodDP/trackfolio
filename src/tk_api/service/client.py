import asyncio
from decimal import Decimal, DivisionByZero, InvalidOperation
from typing import List

from tinkoff.invest import AsyncClient, GetAccountsResponse, InstrumentIdType, InstrumentType, MoneyValue, PortfolioResponse
from tinkoff.invest.async_services import AsyncServices
from tinkoff.invest.utils import decimal_to_quotation, money_to_decimal, quotation_to_decimal

from src.tk_api.schemas import ApiPortfolioPosition, ProportionInPortfolio


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
        self.client = AsyncClient(token=self.token, app_name="trackfolio")
        self.servicies = await self.client.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        return await self.client.__aexit__(exc_type, exc_val, exc_tb)


class AccountService(TinkoffClientService):
    """
    Wrapper for tinkoff.invest.AsyncClient accounts methods.
    Takes responsibility for choosing correct function to call basing on
    sandbox mode flag.
    """

    async def add_money_sandbox(self, account_id: str, money, currency="rub"):
        """Method to add money to sandbox account."""
        money = decimal_to_quotation(Decimal(money))
        if self.sandbox:
            return await self.servicies.sandbox.sandbox_pay_in(
                account_id=account_id,
                amount=MoneyValue(units=money.units,
                                  nano=money.nano, currency=currency),
            )
        else:
            return None

    async def close_sandbox_account(self, account_id: str):
        """Method to close sandbox account by account_id."""
        if self.sandbox:
            return await self.servicies.sandbox.close_sandbox_account(account_id=account_id)

    async def get_accounts(self) -> GetAccountsResponse:
        """Method to get all client accounts (create sandbox account if there is none)."""
        if self.sandbox:
            sandbox_accounts = await self.servicies.sandbox.get_sandbox_accounts()
            if len(sandbox_accounts.accounts) == 0:
                sandbox_account = await self.servicies.sandbox.open_sandbox_account()
                await self.add_money_sandbox(
                    account_id=sandbox_account.account_id,
                    money=2000000
                )
                await asyncio.sleep(3)
                await self.get_accounts()
            return sandbox_accounts
        return await self.servicies.users.get_accounts()


class PortfolioService(TinkoffClientService):
    def __init__(self, token: str, sandbox: bool = True):
        super().__init__(token, sandbox)
        self.portfolio: PortfolioResponse
        self.portfolio_positions: List[ApiPortfolioPosition]
        self.proportion_in_portfolio = ProportionInPortfolio(
            shares=Decimal(0),
            bonds=Decimal(0),
            etf=Decimal(0),
            currencies=Decimal(0),
            unspecified=Decimal(0)
        )

    async def fetch_portfolio(self, account_id: str) -> None:
        """Method to get account portfolio."""
        if self.sandbox:
            self.portfolio = await self.servicies.sandbox.get_sandbox_portfolio(account_id=account_id)
        else:
            self.portfolio = await self.servicies.operations.get_portfolio(account_id=account_id)

    async def get_positions_info(self) -> List[ApiPortfolioPosition]:
        """Method to get additional info for portfolio positions."""
        format = Decimal('0.0000')
        positions = []
        for position in self.portfolio.positions:

            instrument = (await self.servicies.instruments.get_instrument_by(
                id_type=InstrumentIdType.INSTRUMENT_ID_TYPE_FIGI,
                id=position.figi
            )).instrument

            total = decimal_to_quotation(
                money_to_decimal(position.current_price)
                * quotation_to_decimal(position.quantity)
            )

            proportion_in_portfolio = money_to_decimal(total)\
                / money_to_decimal(self.portfolio.total_amount_portfolio)
            proportion_in_portfolio = proportion_in_portfolio.quantize(format)

            try:
                profit = money_to_decimal(position.current_price) /\
                    money_to_decimal(position.average_position_price) - 1
                profit = profit.quantize(format)
            except (DivisionByZero, InvalidOperation):
                profit = None

            try:
                profit_fifo = money_to_decimal(position.current_price) /\
                    money_to_decimal(position.average_position_price_fifo) - 1
                profit_fifo = profit_fifo.quantize(format)
            except (DivisionByZero, InvalidOperation):
                profit_fifo = None

            positions.append(
                ApiPortfolioPosition(
                    ticker=instrument.ticker,
                    name=instrument.name,
                    total=MoneyValue(
                        units=total.units,
                        nano=total.nano,
                        currency=position.current_price.currency
                    ),
                    proportion=Decimal(0.1234).quantize(format),
                    proportion_in_portfolio=proportion_in_portfolio,
                    profit=profit,
                    profit_fifo=profit_fifo,
                    **vars(position)
                )
            )
            self.portfolio_positions = positions
        return positions

    async def get_portfolio_proportions(self):
        format = Decimal('0.00')

        for name in ['shares', 'bonds', 'etf', 'currencies']:
            setattr(
                self.proportion_in_portfolio,
                name,
                (money_to_decimal(getattr(
                    self.portfolio,
                    'total_amount_' + name
                )) / money_to_decimal(self.portfolio.total_amount_portfolio)).quantize(format)
            )

        # for type in InstrumentType:
        #     attr_name = str((type.name)).split('_')[-1].lower() + '_sum'
        #     print(type.name)
        #     setattr(
        #         self,
        #         attr_name,
        #         Decimal(sum(
        #             map(
        #                 lambda position: money_to_decimal(position.total)
        #                 if position.instrument_type == type.name.split('_')[-1].lower()
        #                 else 0,
        #                 self.portfolio_positions
        #             )
        #         )).quantize(format)
        #     )
        attrs = vars(self.proportion_in_portfolio)
        print(attrs)
