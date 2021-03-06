from typing import List, Protocol

from app.core.entities import Transaction


class IAdminRepository(Protocol):
    def fetch_all_transactions(self) -> List[Transaction]:
        pass
