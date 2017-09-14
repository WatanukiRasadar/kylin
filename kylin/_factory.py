from typing import Generic, TypeVar, abstractmethod

T = TypeVar('T')

class Factory(Generic[T]):

  @abstractmethod
  def create(self, **kwargs) -> T: pass
