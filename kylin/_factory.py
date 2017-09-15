from typing import Generic, TypeVar, abstractmethod
from ._register import Register

T = TypeVar('T')

class Factory(Generic[T]):

  @abstractmethod
  def create(self, **kwargs) -> T: pass


@Register(
  name="kylin.decorator.factory"
)
class DecoratorFactory(Factory):

  def create(self, decorator, decorated):
    decorator.decorated = decorated
    return decorator