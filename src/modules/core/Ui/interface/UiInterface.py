from abc import ABC, abstractmethod

class UIComponent(ABC):
    @abstractmethod
    def Draw():
        pass

