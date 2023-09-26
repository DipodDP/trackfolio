from pandas import pandas as pd
from tinkoff.invest import Client, InstrumentIdType, InstrumentType
from tinkoff.invest.caching.instruments_cache.instruments_cache import InstrumentsCache
from tinkoff.invest.caching.instruments_cache.settings import InstrumentsCacheSettings
# from src.tk_api.schemas import ShareSchema
from src.tk_api.service.client import TinkoffClientService


class InstrumentsService(TinkoffClientService):
    """
    Wrapper for tinkoff.invest.AsyncClient instruments methods.
    Takes responsibility for choosing correct function to call basing on
    sandbox mode flag.
    """
    instruments_cache: InstrumentsCache | None = None

    def _store_instruments_cache(self):
        """Function to store instruments cache"""
        with Client(self.token) as client:
            settings = InstrumentsCacheSettings()
            type(self).instruments_cache = InstrumentsCache(
                settings=settings, instruments_service=client.instruments
            )

    async def get_figi_by_ticker(self, ticker: "str") -> tuple[str | None, str | None]:
        """
        Function to get instrument by ticker from stored dataframe or
        from tinkoff-invest API
        """
        # todo: cache dataframe in database or in class attribute
        try:
            df = pd.read_csv('./instruments.csv')
            print(df.head())
        except FileNotFoundError:
            items_list = []
            if not self.instruments_cache:
                self._store_instruments_cache()
            for method in ['shares', 'bonds', 'etfs']:  # , 'currencies', 'futures']:
                for item in getattr(self.instruments_cache, method)().instruments:
                    items_list.append({
                        'ticker': item.ticker,
                        'figi': item.figi,
                        'type': method,
                        'name': item.name,
                    })
            df = pd.DataFrame(items_list)
            df.to_csv('./instruments.csv', index=False)
            print(df.head())
        df = df[df['ticker'] == ticker.upper()]
        if df.empty:
            return (None, None)
        else:
            figi, type = df[['figi', 'type']].iloc[0]
            return (figi, type)

    async def get_instrument_by_ticker(self, ticker: "str"):
        figi, type = await self.get_figi_by_ticker(ticker)
        if figi is not None and type is not None:
            type = type.removesuffix('s')+'_by'
            print(getattr(self.servicies.instruments, type)())
            response = await getattr(self.servicies.instruments, type)(
                id_type=InstrumentIdType.INSTRUMENT_ID_TYPE_FIGI,
                id=figi
            )
            return response

    async def get_instrument_by_figi(self, figi: str):
        response = await self.servicies.instruments.get_instrument_by(
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

    async def instrument_find(self,
                              query: str,
                              instrument_kind: InstrumentType | None = None,
                              api_trade_available_flag: bool | None = None):
        response = await self.servicies.instruments.find_instrument(
            query=query,
            instrument_kind=instrument_kind,
            api_trade_available_flag=api_trade_available_flag
        )
        return response
