from abc import ABC, abstractmethod

class BaseAction(ABC):

    def __eq__(self, other):
        raise NotImplementedError()
    
    def __hash__(self):
        raise NotImplementedError()