from quart import g

from ._context import Context
from ._exceptions import ServiceNotFoundException


class Scope(Context):
    """
        class to register scopes of application
        is singleton to request
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.context = Context()

    def __getitem__(self, item: str):
        if item not in self.keys() and item in self.context.keys():
            self[item] = self.context[item]()
        if item not in self.keys():
            raise ServiceNotFoundException(item)
        return super().get(item)

    def __new__(cls, *args, **kwargs):
        if not hasattr(g, '__scope__'):
            g.__scope__ = dict.__new__(cls)
        return g.__scope__
