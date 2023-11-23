from decimal import Decimal, DivisionByZero, InvalidOperation
import operator
from typing import Literal
from tinkoff.invest import MoneyValue
from tinkoff.invest.utils import decimal_to_quotation, money_to_decimal

from src.tk_api.schemas import HighRiskPart, LowRiskPart, PortfolioRiskParts
from src.tk_api.service.client import PortfolioService


def money_decimal_operation(money: MoneyValue, decimal: Decimal, op: Literal['+', '-', '*', '/']):
    operator_map = {
        '+': operator.add,
        '-': operator.sub,
        '*': operator.mul,
        '/': operator.truediv,
    }
    decimal_money = operator_map[op](
        money_to_decimal(money).quantize(Decimal('0.00')),
        decimal
    )
    return MoneyValue(
        currency=money.currency,
        **vars(decimal_to_quotation(decimal_money))
    )


class PortfolioStructure:
    """
    Structure of the portfolio
    """

    def __init__(
            self,
            client: PortfolioService,
            risk_profile=Decimal('0.35'),
            max_risk_part_drawdown=Decimal('0.5'),
            corp_bonds_proportion=Decimal('0.4'),
            shares_proportion=Decimal('0.8')
        ):
        self.total_amount = client.portfolio.total_amount_portfolio
        self.total_amount_assets = money_decimal_operation(
            self.total_amount,
            money_to_decimal(client.portfolio.total_amount_currencies),
            '-'
        )

        self.risk_profile = risk_profile
        self.max_risk_part_drawdown = max_risk_part_drawdown
        self.risk_proportion = risk_profile/max_risk_part_drawdown
        self.corp_bonds_proportion = corp_bonds_proportion
        self.shares_proportion = shares_proportion
        # try to use DI here, but maybe it's a little dumb implementation here:)
        self.current_structure = PortfolioRiskParts()
        self.current_structure.calculate_current_structure(
            self._get_current_low_risk_part,
            self._get_current_high_risk_part,
            client
        )
        self.plan_structure = PortfolioRiskParts()
        self.plan_structure.calculate_plan_structure(
            self._get_plan_low_risk_part,
            self._get_plan_high_risk_part,
        )

    def _get_current_low_risk_part(self, client: PortfolioService) -> LowRiskPart:
        """
        Method to get structure of the low risk portfolio part
        """
        format = Decimal('0.0000')
        try:
            corp_bonds_proportion = money_to_decimal(
                money_decimal_operation(
                    client.portfolio.total_amount_bonds,
                    money_to_decimal(client.portfolio.total_amount_bonds),
                    '/'
                )
            ).quantize(format)
            gov_bonds_proportion = 1 - corp_bonds_proportion
        except (DivisionByZero, InvalidOperation):
            gov_bonds_proportion = None
            corp_bonds_proportion = None

        gov_bonds_amount = MoneyValue(currency='rub', units=0, nano=0)
        corp_bonds_amount = client.portfolio.total_amount_bonds
        low_risk_total_amount = money_decimal_operation(
            corp_bonds_amount,
            money_to_decimal(gov_bonds_amount),
            '+'
        )
        total_amount_assets = money_decimal_operation(
            self.total_amount,
            money_to_decimal(client.portfolio.total_amount_currencies),
            '-'
        )
        try:
            low_risk_total_proportion = money_to_decimal(
                money_decimal_operation(
                    low_risk_total_amount,
                    money_to_decimal(total_amount_assets),
                    "/"
                )
            ).quantize(format)
        except (DivisionByZero, InvalidOperation):
            low_risk_total_proportion = None
        return LowRiskPart(
            gov_bonds_proportion=gov_bonds_proportion,
            corp_bonds_proportion=corp_bonds_proportion,
            gov_bonds_amount=gov_bonds_amount,
            corp_bonds_amount=corp_bonds_amount,
            low_risk_total_amount=low_risk_total_amount,
            low_risk_total_proportion=low_risk_total_proportion
        )

    def _get_current_high_risk_part(self, client: PortfolioService) -> HighRiskPart:
        """
        Method to get structure of the high risk portfolio part
        """
        format = Decimal('0.0000')
        try:
            shares_proportion = money_to_decimal(
                money_decimal_operation(
                    client.portfolio.total_amount_shares,
                    money_to_decimal(client.portfolio.total_amount_shares) +
                    money_to_decimal(client.portfolio.total_amount_etf),
                    '/'
                )
            ).quantize(format)
            etf_proportion = 1 - shares_proportion
        except (DivisionByZero, InvalidOperation):
            shares_proportion = None
            etf_proportion = None

        shares_amount = client.portfolio.total_amount_shares
        etf_amount = client.portfolio.total_amount_etf
        high_risk_total_amount = money_decimal_operation(
            shares_amount,
            money_to_decimal(etf_amount),
            '+'
        )
        total_amount_assets = money_decimal_operation(
            self.total_amount,
            money_to_decimal(client.portfolio.total_amount_currencies),
            '-'
        )
        try:
            high_risk_total_proportion = money_to_decimal(
                money_decimal_operation(
                    high_risk_total_amount,
                    money_to_decimal(total_amount_assets),
                    "/"
                )
            ).quantize(format)
        except (DivisionByZero, InvalidOperation):
            high_risk_total_proportion = None

        return HighRiskPart(
            etf_proportion=etf_proportion,
            shares_proportion=shares_proportion,
            etf_amount=etf_amount,
            shares_amount=shares_amount,
            high_risk_total_amount=high_risk_total_amount,
            high_risk_total_proportion=high_risk_total_proportion
        )

    def _get_plan_low_risk_part(self) -> LowRiskPart:
        """
        Method to get plan structure of the low risk portfolio part
        """
        format = Decimal('0.0000')
        low_risk_total_amount = money_decimal_operation(
            self.total_amount_assets,
            1-self.risk_proportion,
            '*'
        )
        gov_bonds_proportion = 1 - self.corp_bonds_proportion
        corp_bonds_amount = money_decimal_operation(
            low_risk_total_amount,
            self.corp_bonds_proportion,
            '*'
        )
        gov_bonds_amount = money_decimal_operation(
            low_risk_total_amount,
            gov_bonds_proportion,
            '*'
        )
        try:
            low_risk_total_proportion = money_to_decimal(
                money_decimal_operation(
                    low_risk_total_amount,
                    money_to_decimal(self.total_amount_assets),
                    "/"
                )
            ).quantize(format)
        except (DivisionByZero, InvalidOperation):
            low_risk_total_proportion = None

        return LowRiskPart(
            gov_bonds_proportion=gov_bonds_proportion,
            corp_bonds_proportion=self.corp_bonds_proportion,
            gov_bonds_amount=gov_bonds_amount,
            corp_bonds_amount=corp_bonds_amount,
            low_risk_total_amount=low_risk_total_amount,
            low_risk_total_proportion=low_risk_total_proportion
        )

    def _get_plan_high_risk_part(self) -> HighRiskPart:
        """
        Method to get plan structure of the high risk portfolio part
        """
        format = Decimal('0.0000')
        high_risk_total_amount = money_decimal_operation(
            self.total_amount_assets,
            self.risk_proportion,
            '*'
        )
        etf_proportion = 1 - self.shares_proportion
        etf_amount = money_decimal_operation(
            high_risk_total_amount,
            etf_proportion,
            '*'
        )
        shares_amount = money_decimal_operation(
            high_risk_total_amount,
            self.shares_proportion,
            '*'
        )
        try:
            high_risk_total_proportion = money_to_decimal(
                money_decimal_operation(
                    high_risk_total_amount,
                    money_to_decimal(self.total_amount_assets),
                    "/"
                )
            ).quantize(format)
        except (DivisionByZero, InvalidOperation):
            high_risk_total_proportion = None

        return HighRiskPart(
            etf_proportion=etf_proportion,
            shares_proportion=self.shares_proportion,
            etf_amount=etf_amount,
            shares_amount=shares_amount,
            high_risk_total_amount=high_risk_total_amount,
            high_risk_total_proportion=high_risk_total_proportion
        )
