from abc import ABC, abstractmethod
from typing import Any

class AbstractView(ABC):
    
    @abstractmethod
    def show(self, *args: Any, **kwargs: Any) -> None | Any:
        pass