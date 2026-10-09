"""Omni-Edu model-calling toolkit.

    from omniedu import OmniEdu

    model = OmniEdu.from_pretrained("4B", base_url="http://127.0.0.1:8000/v1")
    print(model.chat(text="求解 x^2 - 5x + 6 = 0", task="solve_reasoned").text)
"""

from .api import OmniEdu
from .tasks import Task, get_task, list_tasks, register_task
from .types import ChatResponse, GenerationParams, Message

__version__ = "0.1.0"

__all__ = [
    "ChatResponse",
    "GenerationParams",
    "Message",
    "OmniEdu",
    "Task",
    "__version__",
    "get_task",
    "list_tasks",
    "register_task",
]

