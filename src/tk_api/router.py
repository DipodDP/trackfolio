from fastapi import APIRouter
from tinkoff.invest import InstrumentIdType

from src.config import settings
from src.tk_api.schemas import ClientAccounts, SandboxTopupRequest
from src.tk_api.service.client import AccountService, TinkoffClientService
from src.tk_api.service.instruments import InstrumentsService

# Account
if settings.sandbox:
    TOKEN = settings.sandbox_invest_token
    ACCOUNT_ID = '482ad8a0-55a2-4a3d-9487-26c7fa3b5296'
else:
    TOKEN = settings.invest_token
    ACCOUNT_ID = '2168069710'

# todo: delete
print(TOKEN)
print(ACCOUNT_ID)

router = APIRouter()


@router.get('/client')
async def get_client() -> ClientAccounts:
    async with AccountService(TOKEN, settings.sandbox) as client:
        accounts = await client.get_accounts()
    return ClientAccounts(
        accounts=accounts.accounts
    )


@router.get('/portfolio')
async def get_portfolio():
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


@router.post('/sandbox')
async def sandbox_topup(request: SandboxTopupRequest):
    async with AccountService(TOKEN, settings.sandbox) as client:
        response = await client.add_money_sandbox(ACCOUNT_ID, request.amount)
    return response

# @router.get('/portfolio/currencies')
# async def get_currencies():
#     async with TinkoffClientService(TOKEN, settings.sandbox) as client:
#         currencies = await client.servicies.instruments.currencies(
#             instrument_status=InstrumentStatus.INSTRUMENT_STATUS_BASE
#         )
#     return currencies
