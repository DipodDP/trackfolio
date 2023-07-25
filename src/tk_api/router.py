from typing import List
from fastapi import APIRouter
from tinkoff.invest import Account, AsyncClient

from src.config import settings
# from src.tk_api.schemas import ClientAccount

# Account
TOKEN = settings.invest_token
router = APIRouter()


@router.get('/client')
async def get_client():
    async with AsyncClient(TOKEN) as client:
        accounts = await client.users.get_accounts()

    return accounts.accounts
