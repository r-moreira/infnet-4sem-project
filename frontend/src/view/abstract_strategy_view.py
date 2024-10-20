from abc import abstractmethod
from view.abstract_view import AbstractView
from enums.view_strategy import ViewStrategy

class AbstractStrategyView(AbstractView):
    
    @abstractmethod
    def accept(self, view: ViewStrategy) -> bool:
        pass