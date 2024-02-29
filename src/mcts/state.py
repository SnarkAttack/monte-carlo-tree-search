from __future__ import annotations
import random
from abc import ABC, abstractmethod

from .action import BaseAction

class BaseState(ABC):

    @abstractmethod
    def get_current_player(self):
        raise NotImplementedError()

    @abstractmethod
    def get_possible_actions(self):
        raise NotImplementedError()
    
    @abstractmethod
    def take_action(self, action: BaseAction) -> BaseState:
        raise NotImplementedError()
    
    @abstractmethod
    def is_terminal(self) -> bool:
        raise NotImplementedError()
    
    @abstractmethod
    def get_reward(self) -> float:
        raise NotImplementedError()
    
    def take_random_action(self):
        random_action = random.choice(self.get_possible_actions())
        return self.take_action(random_action)