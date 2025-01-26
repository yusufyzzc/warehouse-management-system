from typing import Callable, Dict, List


class EventBus:
    """A simple event bus that allows registration and emission of events."""

    def __init__(self):
        # event_name -> list of callbacks
        self.listeners: Dict[str, List[Callable]] = {}

    def register_listener(self, event_name: str, callback: Callable):
        if event_name not in self.listeners:
            self.listeners[event_name] = []
        self.listeners[event_name].append(callback)

    def emit(self, event_name: str, **kwargs):
        if event_name in self.listeners:
            for callback in self.listeners[event_name]:
                callback(**kwargs)
                