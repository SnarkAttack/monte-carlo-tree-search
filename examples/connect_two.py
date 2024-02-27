from copy import deepcopy

from mcts.tree import BaseTree
from mcts.state import BaseState
from mcts.action import BaseAction

class ConnectTwoAction(BaseAction):

    def __init__(self, player, index):
        self.player = player
        self.index = index

    def __hash__(self):
        return hash((self.player, self.index))
    
    def __str__(self):
        return f'Player {self.player} to index {self.index}'


class ConnectTwoState(BaseState):

    def __init__(self):
        
        self.players = {1: 'X',
                        -1: 'O',
                        0: '-'}
        
        self.curr_player = 1
        
        self.board = [0, 0, 0, 0]
        
    def get_current_player(self):
        return self.curr_player

    def get_possible_actions(self):

        possible_actions = []

        for i in range(len(self.board)):
            if self.board[i] == 0:
                possible_actions.append(ConnectTwoAction(self.curr_player, i))

        return possible_actions
    
    def take_action(self, action: BaseAction) -> BaseState:
        next_state = deepcopy(self)
        next_state.board[action.index] = action.player
        next_state.curr_player = action.player * -1
        return next_state
    
    def winner(self):
        for i in range(len(self.board)-1):
            if self.board[i] != 0 and self.board[i] == self.board[i+1]:
                return self.board[i]
        return 0
    
    def is_terminal(self) -> bool:
        return self.winner() != 0 or not any([self.board[i] == 0 for i in range(len(self.board))])

    def get_reward(self) -> float:
        return self.winner()
    
    def visualize_board(self) -> None:
        board = [self.players[self.board[i]] for i in range(len(self.board))]
        print(board)
    
if __name__ == "__main__":

    state = ConnectTwoState()

    decision_tree = BaseTree(state)

    best_action = decision_tree.select_best_action_iterations(1000)

