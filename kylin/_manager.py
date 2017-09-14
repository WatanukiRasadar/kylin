from typing import Generic, TypeVar

T = TypeVar('T')

class Manager(Generic[T]):
  
  def save(self, subject: T) -> T: pass

  def delete(self, subject: T) -> T: pass