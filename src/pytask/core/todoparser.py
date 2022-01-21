from typing import List, Tuple
from venv import create
from .task import Task
import re
from datetime import date


TASK_PREFIX_MATCHER = re.compile(
    r"(?P<done>x )?(\((?P<pri>[A-Z])\) )?((?P<created>\d{4}-\d{2}-\d{2}) )?"
)

CONTEXT_MATCHER = re.compile(r" @(\S+)")
PROJECT_MATCHER = re.compile(r" \+(\S+)")


class TodoParser:
    def __init__(self, stream):
        self._stream = stream

    def extract_tags(self, tag_pattern, line):
        matches = tag_pattern.findall(line)
        return set(matches)

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

            contexts = self.extract_tags(CONTEXT_MATCHER, line)
            projects = self.extract_tags(PROJECT_MATCHER, line)

            tasks.append(
                Task(
                    description=line,
                    priority=priority,
                    is_done=done,
                    created_date=created,
                    contexts=contexts,
                    projects=projects,
                )
            )

        return tasks
