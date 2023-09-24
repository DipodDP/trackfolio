from fastapi import APIRouter

from src.config import settings
from src.tk_api.schemas import Account, ClientAccounts, OrderRequest, Portfolio, SandboxTopupRequest, TotalAmountPortfolio
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
    accounts = ClientAccounts(accounts=[])
    async with AccountService(TOKEN, settings.sandbox) as client:
        response = await client.get_accounts()
    for account in response.accounts:
        accounts.accounts.append(Account(
            id=account.id,
            type=account.type,
            name=account.name,
            status=account.status,
            opened_date=account.opened_date,
            closed_date=account.closed_date,
            access_level=account.access_level
        ))
    return ClientAccounts(
        accounts=accounts.accounts
    )


@router.get('/portfolio')
async def get_portfolio():
    portfolio = Portfolio(
        positions=[],
        total_amount_portfolio=TotalAmountPortfolio()
        
    )
    async with AccountService(TOKEN, settings.sandbox) as client:
        portfoio = await client.get_portfolio(ACCOUNT_ID)
    return portfoio


@router.get('/portfolio/{figi}')
async def get_instrument(figi: str):
    async with InstrumentsService(TOKEN, settings.sandbox) as client:
        instrument = await client.get_share(figi)
    return instrument


@router.get('/ticker/{ticker}')
async def get_instrument_by_ticker(ticker: str):
    async with InstrumentsService(TOKEN, settings.sandbox) as client:
        instrument = await client.get_instrument_by_ticker(ticker)
    return instrument


@router.get('/find/{query}')
async def find_instrument(query: str):
    async with InstrumentsService(TOKEN, settings.sandbox) as client:
        instrument = await client.instrument_find(query)
    return instrument


@router.post('/sandbox')
async def sandbox_topup(request: SandboxTopupRequest):
    async with AccountService(TOKEN, settings.sandbox) as client:
        response = await client.add_money_sandbox(ACCOUNT_ID, request.amount)
    return response


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

# @router.get('/portfolio/currencies')
# async def get_currencies():
#     async with TinkoffClientService(TOKEN, settings.sandbox) as client:
#         currencies = await client.servicies.instruments.currencies(
#             instrument_status=InstrumentStatus.INSTRUMENT_STATUS_BASE
#         )
#     return currencies
