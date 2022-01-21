from datetime import date
from typing import Dict, Set


class Task:
    def __init__(
        self,
        description: str,
        priority: str = None,
        is_done: bool = False,
        created_date: date = date.today(),
        contexts: Set[str] = set(),
        projects: Set[str] = set(),
        completed_date: date = None,
        custom_metadata: Dict[str, str] = {},
    ):
        self.description = description
        self.priority = priority
        self.is_done = is_done
        self.created_date = created_date
        self.contexts = contexts
        self.projects = projects
        self.completed_date = completed_date
        self.custom_metadata = custom_metadata
