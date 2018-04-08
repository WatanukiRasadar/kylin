from abc import ABC, abstractmethod
from asyncio import sleep, wait, get_event_loop


class Processor(ABC):

    @property
    def loop(self): return get_event_loop()

    def __init__(self, name: str, workers: int = 1):
        self.name = name
        self.workers = workers
        self.running = True

    def kill(self): self.running = False

    @abstractmethod
    async def start(self): pass


class TimerProcessor(Processor):

    def __init__(self, sleep_time: int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sleep_time = sleep_time
        self.loop.call_soon(self.start)

    async def start(self):
        print('Starting processors: %s' % self.name)
        while self.running:
            try:
                tasks = [self.run() for i in range(self.workers)]
                await wait(tasks)
            except: self.kill()
            await sleep(self.sleep_time)
        print('Stopping processors: %s' % self.name)

    @abstractmethod
    async def run(self): pass


class EventProcessor(Processor):

    instances = []

    def __init__(self, event_type: type, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.event_type = event_type
        self.events = []
        self.instances.append(self)

    async def start(self):
        print('Starting listeners: %s' % self.name)
        while len(self.events) != 0:
            try:
                tasks = [self.handle_event(self.events.pop()) for i in range(self.workers) if self.events]
                await wait(tasks)
            except: self.kill()
        print('Stopping listeners: %s' % self.name)

    @abstractmethod
    async def handle_event(self, event): pass

    @classmethod
    def get_event_listeners(cls, event):
        return [listener for listener in cls.instances if listener.event_type is type(event)]