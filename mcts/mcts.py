import numpy as np

# constants


# classes

class Board:
    def __init__(self, size = 19):
        self.board = np.zeros((size, size))


class GameState:
    def __init__(self, board = None, liberties = None, n = 19, current_player = 1, black_captures = 0, white_captures = 0, game_ended = False):
        self.n = n
        self.current_player = current_player # 1 or -1
        self.black_captures = black_captures
        self.white_captures = white_captures # TODO take these into account
        self.game_ended = game_ended
        if board == None:
            self.board = np.zeros((n, n))
            self.liberties = np.zeros((n, n))
        else:
            self.board = board
            if liberties == None:
                self.liberties = np.zeros((n, n))
                self.update_liberties()
            else:
                self.liberties = liberties

    def compute_num_of_liberties(self, x, y, stones, liberties = None):
        if liberties is None:
            liberties = set()
        if (x, y) in stones:
            return 0
        stones.add((x, y))
        if x - 1 >= 0:
            if self.board[x - 1][y] == 0:
                liberties.add((x - 1, y))
            elif self.board[x][y] == self.board[x - 1][y]:
                self.compute_num_of_liberties(x - 1, y, stones, liberties)
        if x + 1 < self.n:
            if self.board[x + 1][y] == 0:
                liberties.add((x + 1, y))
            elif self.board[x][y] == self.board[x + 1][y]:
                self.compute_num_of_liberties(x + 1, y, stones, liberties)
        if y - 1 >= 0:
            if self.board[x][y - 1] == 0:
                liberties.add((x, y - 1))
            elif self.board[x][y] == self.board[x][y - 1]:
                self.compute_num_of_liberties(x, y - 1, stones, liberties)
        if y + 1 < self.n:
            if self.board[x][y + 1] == 0:
                liberties.add((x, y + 1))
            elif self.board[x][y] == self.board[x][y + 1]:
                self.compute_num_of_liberties(x, y + 1, stones, liberties)
        return len(liberties)

    def set_chain_liberties(self, x, y, lib, stones = None):
        if stones is None:
            stones = set()
        if (x, y) in stones:
            return
        self.liberties[x][y] = lib
        stones.add((x, y))
        if x - 1 >= 0 and self.board[x][y] == self.board[x - 1][y]:
            self.set_chain_liberties(x - 1, y, lib, stones)
        if x + 1 < self.n and self.board[x][y] == self.board[x + 1][y]:
            self.set_chain_liberties(x + 1, y, lib, stones)
        if y - 1 >= 0 and self.board[x][y] == self.board[x][y - 1]:
            self.set_chain_liberties(x, y - 1, lib, stones)
        if y + 1 < self.n and self.board[x][y] == self.board[x][y + 1]:
            self.set_chain_liberties(x, y + 1, lib, stones)

    def update_liberties(self):
        stones = set()
        for i in range(self.n):
            for j in range(self.n):
                if self.board[i][j] == 0:
                     self.liberties[i][j] = 0
                elif (i, j) not in stones:
                    lib = self.compute_num_of_liberties(i, j, stones)
                    self.set_chain_liberties(i, j, lib)

    def have_same_color(self, x1, y1, x2, y2):
        return self.board[x1][y1] == self.board[x2][y2]

    def inside_board(self, x, y):
        return x >= 0 and x < self.n and y >= 0 and y < self.n

    def legal_move(self, x, y):
        # inside board limits
        if not self.inside_board(x, y):
            return False
        # is an empty intersection
        if self.board[x][y] != 0:
            return False
        # self-atari
        if self.inside_board(x - 1, y) and self.have_same_color(x, y, x - 1, y) and self.liberties[x - 1][y] == 1:
            return False
        if self.inside_board(x + 1, y) and self.have_same_color(x, y, x + 1, y) and self.liberties[x + 1][y] == 1:
            return False
        if self.inside_board(x, y - 1) and self.have_same_color(x, y, x, y - 1) and self.liberties[x][y - 1] == 1:
            return False
        if self.inside_board(x, y + 1) and self.have_same_color(x, y, x, y + 1) and self.liberties[x][y + 1] == 1:
            return False
        # TODO ilegal ko recapture
        return True

    def compute_capture(self, x, y):
        if self.board[x][y] == 1:
            self.black_captures += 1
        elif self.board[x][y] == -1:
            self.white_captures += 1
        else:
            raise Exception('cannot capture an empty intersection')
        self.board[x][y] = 0

    def remove_captured_stones(self, x, y, stones = None):
        if stones is None:
            stones = set()
        # remove stone
        self.compute_capture(x, y)
        stones.add((x,y))
        # check neighboors (connected stones)
        if self.inside_board(x - 1, y) and self.have_same_color(x, y, x - 1, y) and (x - 1, y) not in stones:
            self.remove_captured_stones(x - 1, y, stones)
        if self.inside_board(x + 1, y) and self.have_same_color(x, y, x + 1, y) and (x + 1, y) not in stones:
            self.remove_captured_stones(x + 1, y, stones)
        if self.inside_board(x, y - 1) and self.have_same_color(x, y, x, y - 1) and (x, y - 1) not in stones:
            self.remove_captured_stones(x, y - 1, stones)
        if self.inside_board(x, y + 1) and self.have_same_color(x, y, x, y + 1) and (x, y + 1) not in stones:
            self.remove_captured_stones(x, y + 1, stones)

    def process_captures_from_last_move(self, x, y):
        # in board, opponent stone and only one liberty
        if self.inside_board(x - 1, y) and not self.have_same_color(x, y, x - 1, y) and self.liberties[x - 1][y] == 1:
            self.remove_captured_stones(x - 1, y)
        if self.inside_board(x + 1, y) and not self.have_same_color(x, y, x + 1, y) and self.liberties[x + 1][y] == 1:
            self.remove_captured_stones(x + 1, y)
        if self.inside_board(x, y - 1) and not self.have_same_color(x, y, x, y - 1) and self.liberties[x][y - 1] == 1:
            self.remove_captured_stones(x, y - 1)
        if self.inside_board(x, y + 1) and not self.have_same_color(x, y, x, y + 1) and self.liberties[x][y + 1] == 1:
            self.remove_captured_stones(x, y + 1)

    def process_move(self, move):
        if move == 'pass':
            return True
        elif move == 'resign':
            return True # TODO is this really necessary?
        else:
            x, y = move # TODO make this check more robust
        if not self.legal_move(x, y):
            # TODO this should really do this?
            # raise Exception('This is not a legal move.')
            return False
        self.board[x][y] = self.current_player
        self.process_captures_from_last_move(x, y)
        self.update_liberties()
        self.current_player = -self.current_player
        return True

    def get_game_ended(self):
        return self.game_ended

    # TODO
    def is_terminal_state(self):
        pass

    def all_possible_moves(self):
        possible_moves = set()
        for x in range(self.n):
            for y in range(self.n):
                if self.legal_move(x, y):
                    possible_moves.add((x, y))
        return possible_moves

    def copy(self):
        state = GameState(
            board = self.board[:],
            liberties = self.liberties,
            n = self.n,
            current_player = self.current_player,
            black_captures = self.black_captures,
            white_captures = self.white_captures,
            game_ended = self.game_ended)
        return state

class Node:
    def __init__(self, state = GameState(n = 19), origin_move = None):
        self.state = state
        self.origin_move = origin_move
        self.wins = 0
        self.draws = 0 # NOTE how to take this into account?
        self.visits = 0
        # TODO I need to compute both right?
        self.children = [] # NOTE is there a better data structure?
        self.untried_moves = self.all_possible_moves() # NOTE is really better to store it?

    def process_move(self, move):
        self.state.process_move(move)

    def copy(self):
        node  = Node(state = self.state, origin_move = self.origin_move)
        return node

    def copy_like(self, move = None, set_origin_move = True):
        node = Node(self.state.copy(), self.origin_move)
        if move == None: # NOTE to increase performance
            node.untried_moves = self.untried_moves.copy()
        else:
            node.untried_moves = set([move])
        if set_origin_move:
            node.origin_move = move
        return node

    def add_child(self, node):
        self.children.append(node)

    def get_move(self):
        return self.untried_moves.pop()

    def game_ended(self):
        return self.state.get_game_ended()

    def all_possible_moves(self):
        return self.state.all_possible_moves()

    def do_random_move(self):
        move = self.get_move()
        self.process_move(move)
        self.origin_move = move
        self.untried_moves = self.all_possible_moves()

class MCTSPlayer:
    def __init__(self, size = 19, color = 1, max_iter = 10, reuse_subtree = True, tree_policy = 'uct'):
        # NOTE this player uses chinese rules
        # NOTE cannot play handicap games yet
        self.size = size
        self.color = color
        self.max_iter = max_iter
        self.reuse_subtree = reuse_subtree
        self.root_node = Node(GameState(n = self.size))
        self.policies = {
                        'uct' : self.uct,
                        'policy_network' : self.policy_network
                        }
        self.tree_policy = tree_policy

    def process_move(self, move):
        self.state.process_opponent_move(move)

    def uct_select_child(self, node):
        selected_node = None
        best_win_rate = -1
        for nd in node.children:
            win_rate = nd.wins / nd.visits
            if win_rate > best_win_rate:
                selected_node = nd
                best_win_rate = win_rate
        return selected_node

    def uct(self):
        root_node = self.root_node

        for i in range(self.max_iter):
            # Selection
            current = root_node
            if root_node == None:
                print 'empty root'
            if current == None:
                print 'empty current'
            while not current.game_ended() and len(current.untried_moves) == 0:
                current = self.uct_select_child(current)
            # Expansion
            if not current.game_ended() and len(current.untried_moves) > 0:
                move = current.get_move()
                node = current.copy_like(move)
                node.process_move(move)
                current.add_child(node)
                current = node
            else:
                # NOTE there is achance that the algorithm will always come back here?
                pass
            # Simulation
            node = current
            current = current.copy()
            while not current.game_ended():
                current.do_random_move()
            # Backpropagation
            while current != None:
                current.update_statistics()
                current = current.parent

    def policy_network(self):
        pass

    def gen_move(self):
        heuristic = self.policies[self.tree_policy]
        return heuristic()