from typing import Any, List
from pydantic import BaseModel
# from tinkoff.invest import OrderDirection, OrderType, Quotation
# from tinkoff.invest import Account, GetAccountsResponse


class ClientAccounts(BaseModel):
    accounts: List[Any]


class ShareSchema(BaseModel):
    ticker: str = ""
    lot: int = 1
    short_enabled_flag: bool = False
    otc_flag: bool = False
    buy_available_flag: bool = False
    sell_available_flag: bool = False
    api_trade_available_flag: bool = False


class SandboxTopupRequest(BaseModel):
    amount: str | int | float

class OrderRequest(BaseModel):
    account_id: str
    figi: str
    count_lots: int
    # price: Quotation | None
    is_buy: bool
    # order_type: OrderType

# class OrderResponse(BaseModel):

