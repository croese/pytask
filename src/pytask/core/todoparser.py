from typing import List, Tuple
from venv import create
from .task import Task
import re
from datetime import date

PRIORITY_MATCHER = re.compile(r"\(([A-Z])\) ")
CREATED_MATCHER = re.compile(r"(\d{4}-\d{2}-\d{2}) ")

TASK_PREFIX_MATCHER = re.compile(
    r"(?P<done>x )?(\((?P<pri>[A-Z])\) )?((?P<created>\d{4}-\d{2}-\d{2}) )?"
)


class TodoParser:
    def __init__(self, stream):
        self._stream = stream

    def parse(self) -> List[Task]:
        tasks = []
        for line in self._stream:
            line = line.strip()

            done, priority, created = False, None, None

            m = TASK_PREFIX_MATCHER.match(line)
            if m:
                if m.group("done"):
                    done = True
                if m.group("pri"):
                    priority = m.group("pri")
                if m.group("created"):
                    created = date.fromisoformat(m.group("created"))
                line = line[m.end(0) :]

            tasks.append(
                Task(
                    description=line,
                    priority=priority,
                    is_done=done,
                    created_date=created,
                )
            )

        return tasks
