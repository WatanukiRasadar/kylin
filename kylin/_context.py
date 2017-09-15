from threading import current_thread
from weakref import WeakKeyDictionary
from typing import Type, Dict, List
from ._scope import Scope

class Context:
  
  _instances = WeakKeyDictionary()
  services = {}
  
  def __init__(self):
    self.services = {}
    self.scope = getattr(self,'scope',Scope.build_class().DEFAULT)
  
  def __getitem__(self, name: str):
    return self.services.get(name) or self.instaciate(name, self.__class__.services.get(name))
  
  def instaciate(self,name: str, service: Type):
    instance = service()
    if instance:
      decorators = self.get_decorators(name, service).get(self.scope)
      if decorators:
        for decorator in reversed(decorators.copy()):
          name_factory = '%s.factory' % decorator
          decorator_factory = self[name_factory] if name_factory in self.__class__.services.keys() else self['kylin.decorator.factory']
          instance = decorator_factory.create(decorator=self[decorator],decorated=instance)
    return instance

  def get_decorators(self, name: str, service: Type) -> Dict[Scope, List[str]]:
      return service._decorators
  
  def __new__(cls, *args, **kwargs):
    thread = current_thread()
    instance = cls._instances.get(thread)
    if not instance:
      instance = object.__new__(cls)
      cls._instances[thread] = instance
    return instance
