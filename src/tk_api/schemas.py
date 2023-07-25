from typing import List
from pydantic import BaseModel
import pydantic
from tinkoff.invest import Account, AccountType, GetAccountsResponse


@pydantic.dataclasses.dataclass
class ClientAccounts(Account):
   ... 
