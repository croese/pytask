from typing import List
from .task import Task
import re

PRIORITY_MATCHER = re.compile(r"\(([A-Z])\) ")


class TodoParser:
    def __init__(self, stream):
        self._stream = stream

    def check_done(self, line):
        done = line.startswith("x ")
        line = line[2:] if done else line
        return done, line

    def check_priority(self, line):
        priority = None
        m = PRIORITY_MATCHER.match(line)
        if m:
            priority = m.group(1)
            line = line[m.end(0) :]

        return priority, line

    def parse(self) -> List[Task]:
        tasks = []
        for line in self._stream:
            line = line.strip()

            done, line = self.check_done(line)
            priority, line = self.check_priority(line)

            tasks.append(Task(description=line, priority=priority, is_done=done))

        return tasks
