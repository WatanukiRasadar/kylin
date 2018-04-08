from .._scope import Scope
from .processor import EventProcessor
from asyncio import get_event_loop


class Event:

    def __init__(self):
        self.scope = Scope()

    @property
    def loop(self): return get_event_loop()

    def complete(self):
        return all(self not in listener.events for listener in EventProcessor.get_event_listeners(self))

    def dispatch(self):
        self.scope = Scope()
        for listener in EventProcessor.get_event_listeners(self):
            listener.events.append(self)
            self.loop.call_soon(listener.start)
