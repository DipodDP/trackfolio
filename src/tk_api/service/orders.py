
from tinkoff.invest import OrderDirection, OrderType, PostOrderResponse, Quotation
from src.tk_api.service.client import TinkoffClientService


class OrdersService(TinkoffClientService):
    """
    Wrapper for tinkoff.invest.AsyncClient orders methods.
    Takes responsibility for choosing correct function to call basing on
    sandbox mode flag.
    """

    async def __post_order(
        self,
        account_id: str,
        figi: str,
        count_lots: int,
        price: Quotation | None,
        direction: OrderDirection,
        order_type: OrderType,
        order_id: str
    ) -> PostOrderResponse:
        if self.sandbox:
            return await self.servicies.sandbox.post_sandbox_order(
                figi=figi,
                quantity=count_lots,
                price=price,
                direction=direction,
                account_id=account_id,
                order_type=order_type,
                # order_id=order_id
            )
        # Commented while in development to avoid occasional real order post 

        # return await self.servicies.orders.post_order(
        #     figi=figi,
        #     quantity=count_lots,
        #     price=price,
        #     direction=direction,
        #     account_id=account_id,
        #     order_type=order_type,
        #     order_id=order_id
        # )
    
    async def post_market_order(
        self,
        account_id: str,
        figi: str,
        count_lots: int,
        is_buy: bool
    ) -> PostOrderResponse | None:
        """
        Post market order
        """
        # logger.info(
        #     f"Post market order account_id: {account_id}, "
        #     f"figi: {figi}, count_lots: {count_lots}, is_buy: {is_buy}"
        # )
        response = await self.__post_order(
            account_id=account_id,
            figi=figi,
            count_lots=count_lots,
            price=None,
            direction=OrderDirection.ORDER_DIRECTION_BUY if is_buy else OrderDirection.ORDER_DIRECTION_SELL,
            order_type=OrderType.ORDER_TYPE_MARKET,
            order_id='test_id_1'
            # order_id=generate_order_id()
        )
        # logger.debug(f"order_id is {order_id}")
        return response

