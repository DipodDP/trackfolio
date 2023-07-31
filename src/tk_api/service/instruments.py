from typing import List
from pandas import DataFrame
from tinkoff.invest import InstrumentIdType, Share
from src.tk_api.schemas import ShareSchema
from src.tk_api.service.client import TinkoffClientService


class InstrumentsService(TinkoffClientService):
    """
    Wrapper for tinkoff.invest.AsyncClient instruments methods.
    Takes responsibility for choosing correct function to call basing on
    sandbox mode flag.
    """

    # def __init__(self, token: str, sandbox: bool = True):
    #     super().__init__(token, sandbox)
    #     self.instruments: List[Share]

    async def _get_instruments(self) -> List[Share]:
        response = await self.servicies.instruments.shares()
        # todo: cache needed
        return response.instruments

    async def get_instrument_by_ticker(self, ticker: "str"):
        shares = await self._get_instruments()
        
        df = DataFrame(shares)
        df = df[df['ticker'] == ticker.upper()]
        if df.empty:
            return None
        else:
            return df.to_dict()
            return await self.get_share(str(df['figi'].iloc[0]))

    async def get_share(self, figi: str):
        response = await self.servicies.instruments.share_by(
                id_type=InstrumentIdType.INSTRUMENT_ID_TYPE_FIGI,
                id=figi
        )
        share = response.instrument

        return ShareSchema(
            ticker=share.ticker,
            lot=share.lot,
            short_enabled_flag=share.short_enabled_flag,
            otc_flag=share.otc_flag,
            buy_available_flag=share.buy_available_flag,
            sell_available_flag=share.sell_available_flag,
            api_trade_available_flag=share.api_trade_available_flag
        )


# InstrumentService().servicies.instruments

