from functools import wraps
from typing import Callable

from ._scope import Scope


class Injector(Callable):
    """
        class decorator to inject dependencies into a callable decorated function
    """

    def __init__(self, dependencies: dict, fun: Callable):
        self.dependencies = dependencies
        self.fun = fun

    @property
    def scope(self) -> Scope:
        return Scope()

    def __call__(self, *args, **kwargs):
        injections = {}
        for dependency_name, service_name in self.dependencies.items():
            injections[dependency_name] = kwargs.get(dependency_name) or self.scope[service_name]
        kwargs.update(injections)
        return self.fun(*args, **kwargs)


class Inject(Callable):
    """
        class to recive the callable dependencies
    """
    __injector__ = Injector

    def __init__(self, **dependencies):
        self.dependencies = dependencies

    def __call__(self, fun: Callable):
        def call(*args, **kwargs):
            return self.__injector__(self.dependencies, fun).__call__(*args, **kwargs)
        return wraps(fun).__call__(call)
