from ._context import Context


class Service:
    def __init__(self, name: str = None, names: list = None):
        assert bool(name) != bool(names)
        self.names = names or [name]

    @property
    def context(self) -> Context: return Context()

    def __call__(self, service):
        for service_name in self.names:
            self.context[service_name] = service
        return service
