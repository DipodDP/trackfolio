from typing import Any, List
from pandas import DataFrame
from tinkoff.invest import Client, InstrumentIdType, Share
from tinkoff.invest.caching.instruments_cache.instruments_cache import InstrumentsCache
from tinkoff.invest.caching.instruments_cache.settings import InstrumentsCacheSettings
from src.tk_api.schemas import ShareSchema
from src.tk_api.service.client import TinkoffClientService


class InstrumentsService(TinkoffClientService):
    """
    Wrapper for tinkoff.invest.AsyncClient instruments methods.
    Takes responsibility for choosing correct function to call basing on
    sandbox mode flag.
    """
    instruments_cache: InstrumentsCache | None = None

    def _get_instruments_cache(self):
        """Function to get instruments cache"""
        with Client(self.token) as client:
            settings = InstrumentsCacheSettings()
            type(self).instruments_cache = InstrumentsCache(
                settings=settings, instruments_service=client.instruments
            )

    def _get_instruments(self) -> List[Share] | None:
        """Function to get instruments from cache"""
        if not self.instruments_cache:
            print(self.instruments_cache)
            self._get_instruments_cache()
        if self.instruments_cache:
            response = self.instruments_cache.shares()
            return response.instruments
        else:
            return None

    async def get_instrument_by_ticker(self, ticker: "str"):
        """Function to get instrument by ticker"""
        shares = self._get_instruments()
        # todo: maybe it should cache dataframe somehow
        df = DataFrame(shares)
        df = df[df['ticker'] == ticker.upper()]
        if df.empty:
            return None
        else:
            # return df.to_dict()
            return await self.get_share(str(df['figi'].iloc[0]))

    async def get_share(self, figi: str):
        response = await self.servicies.instruments.share_by(
                id_type=InstrumentIdType.INSTRUMENT_ID_TYPE_FIGI,
                id=figi
        )
        return response
        # share = response.instrument
        #
        # return ShareSchema(
        #     ticker=share.ticker,
        #     lot=share.lot,
        #     short_enabled_flag=share.short_enabled_flag,
        #     otc_flag=share.otc_flag,
        #     buy_available_flag=share.buy_available_flag,
        #     sell_available_flag=share.sell_available_flag,
        #     api_trade_available_flag=share.api_trade_available_flag
        # )


# InstrumentService().servicies.instruments

