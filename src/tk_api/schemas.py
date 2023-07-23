from typing import List
from pydantic import BaseModel


class ClientAccounts(BaseModel):
    accounts: List[str]
