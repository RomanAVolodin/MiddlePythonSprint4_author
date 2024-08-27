from typing import List, Optional
from uuid import UUID

from models.persons import Person


class IPersonService:
    def get_by_id(self, person_id: UUID) -> Optional[Person]:
        raise NotImplementedError

    def get_persons(self, page_size: int, page_number: int, query: str | None) -> List[Person]:
        raise NotImplementedError
