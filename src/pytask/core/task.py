class Task:
    def __init__(self, description: str, priority: str = None, is_done: bool = False):
        self.description = description
        self.priority = priority
        self.is_done = is_done
