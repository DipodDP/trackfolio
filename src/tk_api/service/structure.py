from decimal import Decimal, DivisionByZero, InvalidOperation
import operator
from typing import Literal
from tinkoff.invest import MoneyValue
from tinkoff.invest.utils import decimal_to_quotation, money_to_decimal

from src.tk_api.schemas import HighRiskProportion, LowRiskProportion
from src.tk_api.service.client import PortfolioService


def money_decimal_operation(money: MoneyValue, decimal: Decimal, op: Literal['+','-', '*', '/']):
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


class PortfolioStructure():
    """
    Structure of the portfolio
    """
    def __init__(self, client: PortfolioService):
        self.total_amount = client.portfolio.total_amount_portfolio
        self.high_risk_part = self._get_high_risk_proportion(client)
        self.low_risk_part = self._get_low_risk_proportion(client)

    def _get_low_risk_proportion(self, client: PortfolioService):
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
        return LowRiskProportion(
            gov_bonds_proportion=gov_bonds_proportion,
            corp_bonds_proportion=corp_bonds_proportion,
            gov_bonds_amount=gov_bonds_amount,
            corp_bonds_amount=corp_bonds_amount,
            total_amount=money_decimal_operation(
                corp_bonds_amount,
                money_to_decimal(gov_bonds_amount),
                '+'
            )
        )

    def _get_high_risk_proportion(self, client: PortfolioService):
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
        return HighRiskProportion(
            shares_proportion=shares_proportion,
            etf_proportion=etf_proportion,
            shares_amount=shares_amount,
            etf_amount=etf_amount,
            total_amount=money_decimal_operation(
                shares_amount,
                money_to_decimal(etf_amount),
                '+'
            )
        )


class PlanPortfolioStructure():
    """
    Plan structure of the portfolio
    """
    def __init__(self, client: PortfolioService,risk_profile=Decimal('0.35'), max_risk_part_drawdown=Decimal('0.5')):
        self.total_amount = client.portfolio.total_amount_portfolio
        self.risk_profile = risk_profile
        self.max_risk_part_drawdown = max_risk_part_drawdown
        self.risk_proportion = risk_profile/max_risk_part_drawdown

        self.high_risk_part = self._get_high_risk_proportion(
            money_decimal_operation(
                self.total_amount,
                self.risk_proportion,
                '*'
            )
        )
        self.low_risk_part = self._get_low_risk_proportion(
            money_decimal_operation(
                self.total_amount,
                1-self.risk_proportion,
                '*'
            )
        )

    def _get_low_risk_proportion(self, total_amount: MoneyValue, corp_bonds_proportion=Decimal('0.4')):
        """
        Method to get plan structure of the low risk portfolio part
        """
        gov_bonds_proportion = 1 - corp_bonds_proportion
        corp_bonds_amount=money_decimal_operation(
            total_amount,
            corp_bonds_proportion,
            '*'
        )
        gov_bonds_amount=money_decimal_operation(
            total_amount,
            gov_bonds_proportion,
            '*'
        )

        return LowRiskProportion(
            gov_bonds_proportion=gov_bonds_proportion,
            corp_bonds_proportion=corp_bonds_proportion,
            gov_bonds_amount=gov_bonds_amount,
            corp_bonds_amount=corp_bonds_amount,
            total_amount=money_decimal_operation(
                corp_bonds_amount,
                money_to_decimal(gov_bonds_amount),
                '+'
            )
        )

    def _get_high_risk_proportion(self, total_amount: MoneyValue, shares_proportion=Decimal('0.8')):
        """
        Method to get plan structure of the high risk portfolio part
        """
        etf_proportion = 1 - shares_proportion
        etf_amount=money_decimal_operation(
            total_amount,
            etf_proportion,
            '*'
        )
        shares_amount=money_decimal_operation(
            total_amount,
            shares_proportion,
            '*'
        )
        return HighRiskProportion(
            etf_proportion=etf_proportion,
            shares_proportion=shares_proportion,
            etf_amount=etf_amount,
            shares_amount=shares_amount,
            total_amount=money_decimal_operation(
                shares_amount,
                money_to_decimal(etf_amount),
                '+'
            )
        )
