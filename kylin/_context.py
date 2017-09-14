from threading import current_thread
from weakref import WeakKeyDictionary
from typing import Type

class Context:
  
  _instances = WeakKeyDictionary()
  services = {}
  
  def __init__(self):
    self.services = {}
  
  def __getitem__(self, name: str):
    return self.services.get(name) or self.instaciate(name, self.__class__.services.get(name))
  
  def instaciate(self,name: str, service: Type):
    instance = service()
    self.services[name] =  instance
    return instance
  
  def __new__(cls, *args, **kwargs):
    thread = current_thread()
    instance = cls._instances.get(thread)
    if not instance:
      instance = object.__new__(cls)
      cls._instances[thread] = instance
    return instance
