from __future__ import annotations
import math
import random
from typing import Optional, Sequence

from .state import BaseState

class BaseNode():

    def __init__(self, state: BaseState, parent: Optional[BaseNode] = None):

        self._state = state
        self._parent = parent
        self._children = {}
        self._num_visits = 0
        self._total_reward = 0

    @property
    def state(self) -> BaseState:
        """
        The state associated with the given node
        """
        return self._state

    @property
    def parent(self) -> BaseNode:
        """
        Returns parent node if this node is a child, otherwise returns None

        Returns:
            BaseNode: the parent of the this node
        """
        return self._parent
    
    @property
    def children(self):
        """
        List of all child nodes
        """
        return self._children
    
    @property
    def exploration_value(self):
        """
        The component of the upper confidence bound (UCB) score for this node based on
        the number of visits (exploration)
        """
        if self._num_visits == 0:
            return math.inf
        return math.sqrt(math.log(self._parent.num_visits)/self._num_visits)

    @property
    def exploitation_value(self):
        """
        The component of the upper confidence bound (UCB) score for this node based on
        the scores of previous visits (exploitation)
        """
        if self._num_visits == 0:
            return 0
        return self._total_reward / self._num_visits
    
    @property
    def num_visits(self):
        return self._num_visits
    
    @num_visits.setter
    def num_visits(self, n):
        self._num_visits = n
    
    def calculate_current_value(self, C):
        return self.exploitation_value + C * self.exploration_value
    
    @property
    def is_terminal(self):
        return len(self._children) == 0
    
    def _sorted_children(self, key: None = None, reverse: bool = False) -> Sequence[BaseNode]:
        """
        Returns a list of all children. Order of nodes if no comparator function is
        provided is not-guaranteed to have any properties.

        Args: 
            key (optional): A key function to customize sort order
            reverse (bool, optional): Boolean to reverse order of sorted list

        Returns:
            list of nodes sorted based on the sort function

        """
        return sorted(self.children.values(), key=key, reverse=reverse)
    
    def select_best_child(self, C):
        sorted_children = self._sorted_children(key = lambda n: n.calculate_current_value(C), reverse=True)
        return sorted_children[0]
    
    def expand(self):

        possible_actions = self._state.get_possible_actions()

        for action in possible_actions:
            new_state = self._state.take_action(action)
            new_child = BaseNode(new_state, parent=self)
            self.children[action] = new_child

        return random.choice(list(self.children.values()))

        
