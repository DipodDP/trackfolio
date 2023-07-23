from fastapi import APIRouter
from tinkoff.invest import AsyncClient, GetAccountsResponse

from src.config import settings


TOKEN = settings.invest_token
router = APIRouter()


@router.get('/client')
async def get_client() -> GetAccountsResponse:
    async with AsyncClient(TOKEN) as client:
        accounts = await client.users.get_accounts()

    return accounts
