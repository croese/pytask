from datetime import date
from typing import Set


class Task:
    def __init__(
        self,
        description: str,
        priority: str = None,
        is_done: bool = False,
        created_date: date = date.today(),
        contexts: Set[str] = set(),
    ):
        self.description = description
        self.priority = priority
        self.is_done = is_done
        self.created_date = created_date
        self.contexts = contexts
