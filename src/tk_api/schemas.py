from datetime import datetime
from typing import List
from pydantic import BaseModel
from tinkoff.invest import AccessLevel, AccountStatus, AccountType, Instrument, InstrumentShort, InstrumentType, MoneyValue, OrderDirection, OrderExecutionReportStatus, OrderType, PortfolioPosition, Quotation, RealExchange, SecurityTradingStatus
# from tinkoff.invest import OrderDirection, OrderType


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
    type: AccountType
    name: str
    status: AccountStatus
    opened_date: datetime
    closed_date: datetime
    access_level: AccessLevel


class ClientAccounts(BaseModel):
    accounts: List[Account]


# class PortfolioPosition(BaseModel):
#     figi: str
#     instrument_type: str
#     quantity: Quotation
#     average_position_price: MoneyValue
#     expected_yield: Quotation
#     current_nkd: MoneyValue
#     average_position_price_pt: Quotation
#     current_price: MoneyValue
#     average_position_price_fifo: MoneyValue
#     quantity_lots: Quotation
#     blocked: bool
#     blocked_lots: Quotation
#     position_uid: str
#     instrument_uid: str
#     var_margin: MoneyValue
#     expected_yield_fifo: Quotation


class Portfolio(BaseModel):
    # total_amount_shares: MoneyValue
    # total_amount_bonds: MoneyValue
    # total_amount_etf: MoneyValue
    # total_amount_currencies: MoneyValue
    # total_amount_futures: MoneyValue
    expected_yield: Quotation
    positions: List[PortfolioPosition]
    account_id: str
    # total_amount_options: MoneyValue
    # total_amount_sp: MoneyValue
    total_amount_portfolio: MoneyValue
    # virtual_positions: List[VirtualPortfolioPosition]


# class Instrument(BaseModel):  # pylint:disable=too-many-instance-attributes
#     figi: str
#     ticker: str
#     class_code: str
#     isin: str
#     lot: int
#     currency: str
#     klong: "Quotation"
#     kshort: "Quotation"
#     dlong: "Quotation"
#     dshort: "Quotation"
#     dlong_min: "Quotation"
#     dshort_min: "Quotation"
#     short_enabled_flag: bool
#     name: str
#     exchange: str
#     country_of_risk: str
#     country_of_risk_name: str
#     instrument_type: str
#     trading_status: "SecurityTradingStatus"
#     otc_flag: bool
#     buy_available_flag: bool
#     sell_available_flag: bool
#     min_price_increment: "Quotation"
#     api_trade_available_flag: bool
#     uid: str
#     real_exchange: "RealExchange"
#     position_uid: str
#     for_iis_flag: bool
#     for_qual_investor_flag: bool
#     weekend_flag: bool
#     blocked_tca_flag: bool
#     instrument_kind: "InstrumentType"
#     first_1min_candle_date: datetime
#     first_1day_candle_date: datetime
#


class InstrumentResponse(BaseModel):
    instrument: Instrument


# FindInstrumentResponse
# class InstrumentShort(BaseModel):
#     isin: str
#     figi: str
#     ticker: str
#     class_code: str
#     instrument_type: str
#     name: str
#     uid: str
#     position_uid: str
#     instrument_kind: InstrumentType
#     api_trade_available_flag: str
#     for_iis_flag: bool
#     first_1min_candle_date: datetime
#     first_1day_candle_date: datetime
#     for_qual_investor_flag: bool
#     weekend_flag: bool
#     blocked_tca_flag: bool


class FindInstrumentResponse(BaseModel):
    instruments: List[InstrumentShort]


class SandboxPayInResponse(BaseModel):
    balance: MoneyValue


# class PostOrderResponse():
#     order_id: str
#     execution_report_status: "OrderExecutionReportStatus"
#     lots_requested: int
#     lots_executed: int
#     initial_order_price: "MoneyValue"
#     executed_order_price: "MoneyValue"
#     total_order_amount: "MoneyValue"
#     initial_commission: "MoneyValue"
#     executed_commission: "MoneyValue"
#     aci_value: "MoneyValue"
#     figi: str
#     direction: "OrderDirection"
#     initial_security_price: "MoneyValue"
#     order_type: "OrderType"
#     message: str
#     initial_order_price_pt: "Quotation"
#     instrument_uid: str
