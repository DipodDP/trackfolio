from decimal import Decimal
from fastapi import APIRouter
from tinkoff.invest import InstrumentIdType, MoneyValue
from tinkoff.invest.utils import decimal_to_quotation, money_to_decimal, quotation_to_decimal
# from tinkoff.invest import InstrumentStatus

from src.config import settings
from src.tk_api.schemas import ApiFindInstrumentResponse, ApiGetAccountsResponse, ApiInstrumentResponse, ApiPortfolioPosition, ApiPortfolioResponse, ApiPostOrderRequest, ApiSandboxPayInRequest, ExtMoneyValue, TrackfolioAccount, SandboxPayInResponse
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
async def get_client() -> ApiGetAccountsResponse:
    async with AccountService(TOKEN, settings.sandbox) as client:
        response = await client.get_accounts()
    accounts = []

    for account in response.accounts:
        accounts.append(TrackfolioAccount(
            id=account.id,
            type=account.type,
            name=account.name,
            status=account.status,
            opened_date=account.opened_date,
            closed_date=account.closed_date,
            access_level=account.access_level
        ))

    return ApiGetAccountsResponse(
        accounts=accounts
    )


@router.get('/portfolio')
async def get_portfolio() -> ApiPortfolioResponse:
    async with AccountService(TOKEN, settings.sandbox) as client:
        response = await client.get_portfolio(ACCOUNT_ID)
        positions = await client.get_positions_info(response)

    return ApiPortfolioResponse(
        positions=positions,
        total_amount_portfolio=response.total_amount_portfolio,
        expected_yield=response.expected_yield,
        account_id=response.account_id
    )


@router.get('/portfolio/{figi}')
async def get_instrument(figi: str) -> ApiInstrumentResponse:
    async with InstrumentsService(TOKEN, settings.sandbox) as client:
        response = await client.get_instrument_by_figi(figi)

    return ApiInstrumentResponse(
        instrument=response.instrument
    )


@router.get('/find')
async def find_instrument(query: str) -> ApiFindInstrumentResponse:
    async with InstrumentsService(TOKEN, settings.sandbox) as client:
        response = await client.instrument_find(query)

    return ApiFindInstrumentResponse(
        instruments=[
            # using List comprehensions to filter
            # results from tinkoff api that not allowed for trading
            instrument for instrument in response.instruments
            if instrument.api_trade_available_flag
        ]
    )


@router.post('/sandbox')
async def sandbox_topup(request: ApiSandboxPayInRequest) -> SandboxPayInResponse:
    async with AccountService(TOKEN, settings.sandbox) as client:
        response = await client.add_money_sandbox(ACCOUNT_ID, request.amount)

    return SandboxPayInResponse(
        balance=response.balance
    )


@router.post('/portfolio')
async def post_market_order(request: ApiPostOrderRequest):
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
