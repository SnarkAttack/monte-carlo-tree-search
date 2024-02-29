import math
import time
from copy import deepcopy
from typing import Optional

from .node import BaseNode
from .state import BaseState

class BaseTree:

    def __init__(self, base_state: BaseState, C: Optional[float] = math.sqrt(2)):

        self._root = BaseNode(base_state)
        self._C = C

    @property
    def num_iterations_run(self):
        return self._root.num_visits

    def _select_node(self, start_node):
        """
        From the current environment state, select the action node to perform
        """
        curr_node = start_node
        while not curr_node.is_terminal:
            curr_node = curr_node.select_best_child(self._C)
        return curr_node

    def _expand_node(self, node_to_expand):
        # Check if this node contains a terminal state before expanding
        if node_to_expand.state.is_terminal():
            return node_to_expand

        child_node = node_to_expand.expand()
        return child_node

    def _simulate_environment(self, node):
        curr_state = node.state
        while not curr_state.is_terminal():
            curr_state = curr_state.take_random_action()

        return curr_state


    def _backpropogate(self, node, reward):
        while node is not None:
            node._total_reward += reward
            node.num_visits += 1
            node = node.parent

    def _evolve_tree_state(self):
        node_to_act_from = self._select_node(self._root)
        child_node = self._expand_node(node_to_act_from)
        random_terminal_state = self._simulate_environment(child_node)
        self._backpropogate(child_node, random_terminal_state.get_reward())

    def sort_possible_actions(self, reverse=False):
        
        children = sorted(self._root.children.items(), key=lambda x: x[1].exploitation_value, reverse=True)
        return children

    def select_best_action_iterations(self, num_iterations, maximal=True):

        for _ in range(num_iterations):
            self._evolve_tree_state()

        best_child = self.sort_possible_actions(reverse=maximal)[0]
        best_action = best_child[0]

        return best_action

    def select_best_action_time(self, ms, maximal=True):
        start_time = time.time()*1000
        while time.time()*1000 < start_time+ms:
            self._evolve_tree_state()

        best_child = self.sort_possible_actions(reverse=maximal)[0]
        best_action = best_child[0]

        return best_action
    
    def create_tree_from_action(self, action):

        action_node = deepcopy(self._root.children[action])

        # action_node.state.display_game_state()

        return BaseTree(action_node.state, C=self._C)


    