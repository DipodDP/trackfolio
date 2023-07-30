from fastapi import APIRouter

from src.config import settings
from src.tk_api.service.client import TinkoffClientService

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
async def get_client():
    async with TinkoffClientService(TOKEN, settings.sandbox) as client:
        accounts = await client.get_accounts()
    return accounts


@router.get('/portfolio')
async def get_portfolio():
    async with TinkoffClientService(TOKEN, settings.sandbox) as client:
        portfoio = await client.get_portfolio(ACCOUNT_ID)
    return portfoio
