from typing import Generic, TypeVar, abstractmethod

T = TypeVar('T')

class Provider(Generic[T]):
  
  @abstractmethod
  def provide(self) -> T: pass
