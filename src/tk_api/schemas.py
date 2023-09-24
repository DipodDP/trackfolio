from datetime import datetime
from typing import Any, List
from pydantic import BaseModel
# from tinkoff.invest import OrderDirection, OrderType, Quotation
# from tinkoff.invest import Account, GetAccountsResponse


# class ClientAccounts(BaseModel):
#     accounts: List[Any]


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


# tinkoff api response schemas

class Account(BaseModel):
    id: str
    type: int
    name: str
    status: int
    opened_date: datetime
    closed_date: datetime
    access_level: int


class ClientAccounts(BaseModel):
    accounts: List[Account]


class TotalAmountShares(BaseModel):
    currency: str
    units: int
    nano: int


class TotalAmountBonds(BaseModel):
    currency: str
    units: int
    nano: int


class TotalAmountEtf(BaseModel):
    currency: str
    units: int
    nano: int


class TotalAmountCurrencies(BaseModel):
    currency: str
    units: int
    nano: int


class TotalAmountFutures(BaseModel):
    currency: str
    units: int
    nano: int


class ExpectedYield(BaseModel):
    units: int
    nano: int


class Quantity(BaseModel):
    units: int
    nano: int


class AveragePositionPrice(BaseModel):
    currency: str
    units: int
    nano: int


class ExpectedYield1(BaseModel):
    units: int
    nano: int


class CurrentNkd(BaseModel):
    currency: str
    units: int
    nano: int


class AveragePositionPricePt(BaseModel):
    units: int
    nano: int


class CurrentPrice(BaseModel):
    currency: str
    units: int
    nano: int


class AveragePositionPriceFifo(BaseModel):
    currency: str
    units: int
    nano: int


class QuantityLots(BaseModel):
    units: int
    nano: int


class BlockedLots(BaseModel):
    units: int
    nano: int


class VarMargin(BaseModel):
    currency: str
    units: int
    nano: int


class ExpectedYieldFifo(BaseModel):
    units: int
    nano: int


class MoneyValue(BaseModel):
    currency: str
    units: int
    nano: int


class Quotation(BaseModel):
    units: int
    nano: int


class Position(BaseModel):
    figi: str
    instrument_type: str
    quantity: Quotation
    average_position_price: MoneyValue
    expected_yield: Quotation
    current_nkd: MoneyValue
    average_position_price_pt: Quotation
    current_price: MoneyValue
    average_position_price_fifo: MoneyValue
    quantity_lots: Quotation
    blocked: bool
    blocked_lots: Quotation
    position_uid: str
    instrument_uid: str
    var_margin: MoneyValue
    expected_yield_fifo: Quotation


class TotalAmountOptions(BaseModel):
    currency: str
    units: int
    nano: int


class TotalAmountSp(BaseModel):
    currency: str
    units: int
    nano: int


class TotalAmountPortfolio(BaseModel):
    currency: str
    units: int
    nano: int


class Portfolio(BaseModel):
    # total_amount_shares: TotalAmountShares
    # total_amount_bonds: TotalAmountBonds
    # total_amount_etf: TotalAmountEtf
    # total_amount_currencies: TotalAmountCurrencies
    # total_amount_futures: TotalAmountFutures
    expected_yield: Quotation
    positions: List[Position]
    account_id: str
    # total_amount_options: TotalAmountOptions
    # total_amount_sp: TotalAmountSp
    total_amount_portfolio: MoneyValue
    # virtual_positions: List
