from ._countext import Context
from ._inject import Inject
from typing import Type

class Register:
  
  def __init__(self, name: str, context: Type[Context]=Context):
    self.name = name
    self.context = context
  
  def __call__(self, service):
    self.context.services[self.name] = service
    return service
