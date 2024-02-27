import math
from typing import Optional

from .node import BaseNode
from .state import BaseState

class BaseTree:

    def __init__(self, base_state: BaseState, C: Optional[float] = math.sqrt(2)):

        self._root = BaseNode(base_state)
        self._C = C

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
            curr_state = curr_state.get_random_next_state()

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

    def select_best_action_iterations(self, num_iterations):

        for _ in range(num_iterations):
            self._evolve_tree_state()

        best_child = sorted(self._root.children.items(), key=lambda x: x[1].exploitation_value, reverse=True)[0]
        best_action = best_child[0]

        return best_action
