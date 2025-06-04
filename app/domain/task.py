from dataclasses import dataclass

@dataclass
class Task:
    id: int = None
    title: str = ''
    description: str = ''
    is_completed: bool = False
