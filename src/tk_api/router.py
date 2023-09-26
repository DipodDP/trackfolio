from fastapi import APIRouter
# from tinkoff.invest import InstrumentStatus

from src.config import settings
from src.tk_api.schemas import Account, ClientAccounts, FindInstrumentResponse, InstrumentResponse, OrderRequest, Portfolio, SandboxPayInResponse, SandboxTopupRequest
from src.tk_api.service.client import AccountService
from src.tk_api.service.instruments import InstrumentsService
from src.tk_api.service.orders import OrdersService

# Account
if settings.sandbox:
    ACCOUNT_ID = settings.sandbox_account_id
    TOKEN = settings.sandbox_invest_token
else:
    ACCOUNT_ID = settings.account_id
    TOKEN = settings.invest_token

# todo: delete
print(TOKEN)
print(ACCOUNT_ID)

router = APIRouter()


@router.get('/client')
async def get_client() -> ClientAccounts:
    async with AccountService(TOKEN, settings.sandbox) as client:
        response = await client.get_accounts()
    accounts = []

    for account in response.accounts:
        accounts.append(Account(
            id=account.id,
            type=account.type,
            name=account.name,
            status=account.status,
            opened_date=account.opened_date,
            closed_date=account.closed_date,
            access_level=account.access_level
        ))

    return ClientAccounts(
        accounts=accounts
    )


@router.get('/portfolio')
async def get_portfolio() -> Portfolio:
    async with AccountService(TOKEN, settings.sandbox) as client:
        response = await client.get_portfolio(ACCOUNT_ID)

    return Portfolio(
        positions=response.positions,
        total_amount_portfolio=response.total_amount_portfolio,
        expected_yield=response.expected_yield,
        account_id=response.account_id
    )


@router.get('/portfolio/{figi}')
async def get_instrument(figi: str) -> InstrumentResponse:
    async with InstrumentsService(TOKEN, settings.sandbox) as client:
        response = await client.get_instrument_by_figi(figi)

    return InstrumentResponse(
        instrument=response.instrument
    )


@router.get('/find/{query}')
async def find_instrument(query: str) -> FindInstrumentResponse:
    async with InstrumentsService(TOKEN, settings.sandbox) as client:
        response = await client.instrument_find(query)

    return FindInstrumentResponse(
        instruments=response.instruments
    )


@router.post('/sandbox')
async def sandbox_topup(request: SandboxTopupRequest) -> SandboxPayInResponse:
    async with AccountService(TOKEN, settings.sandbox) as client:
        response = await client.add_money_sandbox(ACCOUNT_ID, request.amount)

    return SandboxPayInResponse(
        balance=response.balance
    )


@router.post('/portfolio')
async def post_market_order(request: OrderRequest):
    async with OrdersService(TOKEN, settings.sandbox) as client:
        order = await client.post_market_order(
            figi=request.figi,
            account_id=ACCOUNT_ID,
            count_lots=request.count_lots,
            is_buy=request.is_buy
        )

    return order


# @router.get('/ticker/{ticker}')
# async def get_instrument_by_ticker(ticker: str):
#     async with InstrumentsService(TOKEN, settings.sandbox) as client:
#         instrument = await client.get_instrument_by_ticker(ticker)
#
#     return instrument


# @router.get('/portfolio/currencies')
# async def get_currencies():
#     async with AccountService(TOKEN, settings.sandbox) as client:
#         currencies = await client.servicies.instruments.currencies(
#             instrument_status=InstrumentStatus.INSTRUMENT_STATUS_BASE
#         )
#     return currencies
