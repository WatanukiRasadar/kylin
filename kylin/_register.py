from typing import Dict, Type, List
from ._context import Context
from ._inject import Inject
from ._scope import Scope

class Register:
  
  def __init__(self, name: str, context: Type[Context]=Context, decorators:Dict[Scope, List[str]]={}):
    self.name = name
    self.context = context
    self.decorators = decorators
  
  def __call__(self, service):
    service._decorators = self.decorators
    self.context.services[self.name] = service
    return service
