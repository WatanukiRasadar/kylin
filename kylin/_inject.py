from types import FunctionType
from functools import wraps
from ._context import Context

class Inject:
  
  def __init__(self, **dependencies):
    self.dependencies = dependencies
  
  def __call__(self, fun: FunctionType) -> FunctionType:
    @wraps(fun)
    def injector(*args, **runtime_injections):
      context = Context()
      injections = {}
      for param, name in self.dependencies.items():
        injections[param] = context[name]
      injections.update(runtime_injections)
      return fun(*args, **injections)
    return injector