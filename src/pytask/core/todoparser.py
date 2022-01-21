from typing import List, Tuple
from venv import create
from .task import Task
import re
from datetime import date

CONTEXT_MATCHER = re.compile(r" @(\S+)")
PROJECT_MATCHER = re.compile(r" \+(\S+)")
METADATA_MATCHER = re.compile(r"([^:\s]+):([^:\s]+)")

TASK_PREFIX_MATCHER = re.compile(
    r"""(
(?P<done>x\ (?P<completed>\d{4}-\d{2}-\d{2})\ )
|
(\((?P<pri>[A-Z])\)\ )
)?
((?P<created>\d{4}-\d{2}-\d{2})\ )?""",
    re.X,
)


class TodoParser:
    def __init__(self, stream):
        self._stream = stream

    def extract_tags(self, tag_pattern, line):
        matches = tag_pattern.findall(line)
        return set(matches)

    def extract_custom_metadata(self, line):
        matches = METADATA_MATCHER.findall(line)
        return dict(matches)

    def parse(self) -> List[Task]:
        tasks = []
        for line in self._stream:
            line = line.strip()

            done, completed, priority, created = False, None, None, None

            m = TASK_PREFIX_MATCHER.match(line)
            if m:
                if m.group("done"):
                    done = True
                    completed = date.fromisoformat(m.group("completed"))
                if m.group("pri"):
                    priority = m.group("pri")
                if m.group("created"):
                    created = date.fromisoformat(m.group("created"))
                line = line[m.end(0) :]

            contexts = self.extract_tags(CONTEXT_MATCHER, line)
            projects = self.extract_tags(PROJECT_MATCHER, line)
            custom_metadata = self.extract_custom_metadata(line)

            tasks.append(
                Task(
                    description=line,
                    priority=priority,
                    is_done=done,
                    created_date=created,
                    contexts=contexts,
                    projects=projects,
                    completed_date=completed,
                    custom_metadata=custom_metadata,
                )
            )

        return tasks
