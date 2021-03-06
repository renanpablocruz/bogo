from __future__ import division
import numpy as np
import math
from random import shuffle
from utils import *

# NOTE using max_game_length. can I avoid this?

# TODO: incorporate class
# class Board:
#     def __init__(self, size = 19):
#         self.board = np.zeros((size, size), dtype = np.int)

# classes
class GameState:
    def __init__(self, board = None, prev_board = None, liberties = None, n = 19, current_player = 1, black_captures = 0, white_captures = 0, game_ended = False, black_passed = False, white_passed = False, game_length = 0):
        self.n = n
        self.current_player = current_player # 1 or -1
        self.black_captures = black_captures
        self.white_captures = white_captures # TODO take these into account
        self.black_passed = False
        self.white_passed = False
        self.game_ended = game_ended
        self.game_length = game_length
        if board is None: # NOTE numpy will take '== None' as an element-wise operation
            self.board = np.zeros((self.n, self.n), dtype = np.int)
            self.prev_board = np.zeros((self.n, self.n), dtype = np.int) # NOTE cannot have board is None and prev_board not None
            self.liberties = np.zeros((self.n, self.n), dtype = np.int)
        else:
            self.board = board
            if prev_board is None:
                raise Exception('prev_board cannot be None if board is not')
            else:
                self.prev_board = prev_board
            if liberties is None:
                self.liberties = np.zeros((self.n, self.n), dtype = np.int)
                self.update_liberties()
            else:
                self.liberties = liberties

    def compute_num_of_liberties(self, x, y, stones = None, liberties = None):
        if stones == None:
            stones = set()
        if liberties == None:
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
        if stones == None:
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
        for x in range(self.n):
            for y in range(self.n):
                if self.board[x][y] == 0:
                     self.liberties[x][y] = 0
                elif (x, y) not in stones:
                    lib = self.compute_num_of_liberties(x, y)
                    self.set_chain_liberties(x, y, lib, stones)

    def have_same_color(self, x1, y1, x2, y2):
        return self.board[x1][y1] == self.board[x2][y2]

    def inside_board(self, x, y):
        return x >= 0 and x < self.n and y >= 0 and y < self.n

    # NOTE older version
    # def legal_move(self, x, y):
    #     # inside board limits
    #     if not self.inside_board(x, y):
    #         return False
    #     # is an empty intersection
    #     if self.board[x][y] != 0:
    #         return False
    #     # self-atari
    #     if self.inside_board(x - 1, y) and self.have_same_color(x, y, x - 1, y) and self.liberties[x - 1][y] == 1:
    #         print conv_int_to_letters((x, y)), 'is not a valid move'
    #         return False
    #     if self.inside_board(x + 1, y) and self.have_same_color(x, y, x + 1, y) and self.liberties[x + 1][y] == 1:
    #         print conv_int_to_letters((x, y)), 'is not a valid move'
    #         return False
    #     if self.inside_board(x, y - 1) and self.have_same_color(x, y, x, y - 1) and self.liberties[x][y - 1] == 1:
    #         print conv_int_to_letters((x, y)), 'is not a valid move'
    #         return False
    #     if self.inside_board(x, y + 1) and self.have_same_color(x, y, x, y + 1) and self.liberties[x][y + 1] == 1:
    #         print conv_int_to_letters((x, y)), 'is not a valid move'
    #         return False
    #     # TODO ilegal ko recapture
    #     # NOTE how to optimize?
    #     temp = self.copy() # NOTE a Board class would make this easier
    #     temp.process_move_with_no_verification((x, y))
    #     if np.array_equal(self.prev_board, temp):
    #         return False
    #     return True

    def legal_move(self, x, y):
        # inside board limits
        if not self.inside_board(x, y):
            return False
        # is an empty intersection
        if self.board[x][y] != 0:
            return False
        # self-atari
        # if self.inside_board(x - 1, y) and self.board[x - 1][y] == self.current_player and self.liberties[x - 1][y] == 1:
        #     print conv_int_to_letters((x, y)), 'is not a valid move'
        #     return False
        # if self.inside_board(x + 1, y) and self.board[x + 1][y] == self.current_player and self.liberties[x + 1][y] == 1:
        #     print conv_int_to_letters((x, y)), 'is not a valid move'
        #     return False
        # if self.inside_board(x, y - 1) and self.board[x][y - 1] == self.current_player and self.liberties[x][y - 1] == 1:
        #     print conv_int_to_letters((x, y)), 'is not a valid move'
        #     return False
        # if self.inside_board(x, y + 1) and self.board[x][y + 1] == self.current_player and self.liberties[x][y + 1] == 1:
        #     print conv_int_to_letters((x, y)), 'is not a valid move'
        #     return False
        # tempself.
        # NOTE how to optimize? cfeating a Board class? what more?
        temp = self.copy() # NOTE a Board class would make this easier
        temp.process_move_with_no_verification((x, y))
        # self-atari
        if temp.liberties[x][y] == 0:
            return False
        # ilegal ko recapture
        if np.array_equal(self.prev_board, temp):
            return False
        return True

    def is_an_opponent_stone(self, x, y):
        return self.board[x][y] == -self.current_player

    def compute_capture(self, x, y):
        if self.board[x][y] == 1:
            self.white_captures += 1
        elif self.board[x][y] == -1:
            self.black_captures += 1
        else:
            raise Exception('cannot capture an empty intersection, move', conv_int_to_letters((x, y)), self.board[x][y])
        self.board[x][y] = 0

    # previous version
    # def remove_captured_stones(self, x, y, stones = None):
    #     if stones is None:
    #         stones = set()
    #     # remove stone
    #     self.compute_capture(x, y)
    #     stones.add((x,y))
    #     # check neighboors (connected stones)
    #     if self.inside_board(x - 1, y) and self.have_same_color(x, y, x - 1, y) and (x - 1, y) not in stones:
    #         self.remove_captured_stones(x - 1, y, stones)
    #     if self.inside_board(x + 1, y) and self.have_same_color(x, y, x + 1, y) and (x + 1, y) not in stones:
    #         self.remove_captured_stones(x + 1, y, stones)
    #     if self.inside_board(x, y - 1) and self.have_same_color(x, y, x, y - 1) and (x, y - 1) not in stones:
    #         self.remove_captured_stones(x, y - 1, stones)
    #     if self.inside_board(x, y + 1) and self.have_same_color(x, y, x, y + 1) and (x, y + 1) not in stones:
    #         self.remove_captured_stones(x, y + 1, stones)

    def remove_captured_stones(self, x, y):
        # remove stone
        self.compute_capture(x, y)
        # check neighboors (connected stones)
        if self.inside_board(x - 1, y) and self.is_an_opponent_stone(x - 1, y):
            self.remove_captured_stones(x - 1, y)
        if self.inside_board(x + 1, y) and self.is_an_opponent_stone(x + 1, y):
            self.remove_captured_stones(x + 1, y)
        if self.inside_board(x, y - 1) and self.is_an_opponent_stone(x, y - 1):
            self.remove_captured_stones(x, y - 1)
        if self.inside_board(x, y + 1) and self.is_an_opponent_stone(x, y + 1):
            self.remove_captured_stones(x, y + 1)

    def process_captures_from_last_move(self, x, y):
        # in board, opponent stone and only one liberty
        if self.inside_board(x - 1, y) and self.is_an_opponent_stone(x - 1, y) and self.liberties[x - 1][y] == 1:
            debug('player ' + str(self.current_player) + ' capture after playing at ' + conv_int_to_letters((x, y)))
            self.remove_captured_stones(x - 1, y)
        if self.inside_board(x + 1, y) and self.is_an_opponent_stone(x + 1, y) and self.liberties[x + 1][y] == 1:
            debug('capture after playing at ' + conv_int_to_letters((x, y)))
            self.remove_captured_stones(x + 1, y)
        if self.inside_board(x, y - 1) and self.is_an_opponent_stone(x, y - 1) and self.liberties[x][y - 1] == 1:
            debug('capture after playing at ' + conv_int_to_letters((x, y)))
            self.remove_captured_stones(x, y - 1)
        if self.inside_board(x, y + 1) and self.is_an_opponent_stone(x, y + 1) and self.liberties[x][y + 1] == 1:
            debug('capture after playing at ' + conv_int_to_letters((x, y)))
            self.remove_captured_stones(x, y + 1)

    def set_current_player_passed(self, passed):
        if self.current_player == 1:
            self.black_passed = passed
        elif self.current_player == -1:
            self.white_passed = passed
        else:
            raise Exception('not a valid current player', self.current_player)
        if self.black_passed and self.white_passed:
            self.game_ended = True

    def process_move_with_no_verification(self, move):
        x, y = move # TODO make this check more robust
        self.prev_board = np.copy(self.board)
        self.board[x][y] = self.current_player
        self.process_captures_from_last_move(x, y)
        self.update_liberties()
        self.current_player = -self.current_player
        # self.untried_moves = self.all_possible_moves()
        # NOTE check if the game ended?
        # TODO how to do it? probably when get_move returns 'pass' twice!
        return True


    def process_move(self, move):
        self.game_length += 1
        if move == (-1, -1): # pass move
            self.set_current_player_passed(True)
            self.prev_board = np.copy(self.board) # NOTE can I not repeat this code
            self.current_player = -self.current_player
            return True
        # TODO resign option is really here?
        else:
            self.set_current_player_passed(False)
            x, y = move # NOTE do I need to make this check more robust
        if not self.legal_move(x, y):
            # TODO this should really do this?
            raise Exception('This is not a legal move.', move)
            return False
        self.prev_board = np.copy(self.board)
        if (x, y) == (18, 18):
            print 'ss is been played'
        self.board[x][y] = self.current_player
        self.process_captures_from_last_move(x, y)
        self.update_liberties()
        self.current_player = -self.current_player # NOTE it has to be after the board update
        self.untried_moves = self.all_possible_moves()
        # NOTE check if the game ended?
        # TODO how to do it? probably when get_move returns 'pass' twice!
        return True

    # def inside_own_territory(self, x, y, stones = None):
    #     if stones == None:
    #         stones = set()
    #     if (x, y) in stones:
    #         return dsds
    #     stones.add((x, y))
    #     if x - 1 >= 0 and (x - 1, y) not in stones:
    #         if self.board

    def all_possible_moves(self):
        possible_moves = []
        for x in range(self.n):
            for y in range(self.n):
                # temp = self.copy()
                # temp.process_move_with_no_verification((x, y))
                # lib = temp.
                # inside_own_territory =
                # if self.legal_move(x, y) and not inside_own_territory:
                if self.legal_move(x, y):
                    possible_moves.append((x, y))
        shuffle(possible_moves)
        return possible_moves

    def copy(self):
        return GameState(
                board = np.copy(self.board),
                prev_board = np.copy(self.prev_board),
                liberties = np.copy(self.liberties),
                n = self.n,
                current_player = self.current_player,
                black_captures = self.black_captures,
                white_captures = self.white_captures,
                game_ended = self.game_ended,
                black_passed = self.black_passed,
                white_passed = self.white_passed,
                game_length = self.game_length)

    def print_board(self):
        letters = 'abcdefghijklmnopqrstuvwxyz'
        print ' ',
        for i in range(self.n):
            print letters[i],
        print ''
        for i in range(self.n):
            print letters[i],
            for j in range(self.n):
                print player_num_to_symbol(self.board[i][j]),
            print ''

    def print_liberties(self):
        letters = 'abcdefghijklmnopqrstuvwxyz'
        print ' ',
        for i in range(self.n):
            print letters[i],
        print ''
        for i in range(self.n):
            print letters[i],
            for j in range(self.n):
                print str(self.liberties[i][j]),
            print ''

    def get_winner(self): # NOTE only makes sense to call it when game_ended == True
        # BIG TODO how to include the dead stones on the board?
        if self.black_captures > self.white_captures:
            return 1
        elif self.black_captures < self.white_captures:
            return -1
        else:
            return 0

    def do_random_move(self):
        # move = self.get_move()
        options = self.all_possible_moves()
        if len(options) == 0:
            move = (-1, -1)
        else:
            move = options[0]
        debug('trying to play at ' + conv_int_to_letters(move))
        valid_action = self.process_move(move)
        self.print_board()
        self.print_liberties()
        if not valid_action:
            raise Exception('not a valid move', conv_int_to_letters(move))
        return move

class Node:
    def __init__(self, state = None, origin_move = None, children = None, wins = 0, draws = 0, visits = 0, parent = None):
        self.state = GameState() if state == None else state
        self.origin_move = origin_move
        self.wins = wins
        self.draws = draws # NOTE how to take this into account?
        self.visits = visits
        # TODO I need to compute both right?
        # NOTE is there a better data structure?
        self.children = [] if children == None else children
        self.untried_moves = self.all_possible_moves() # NOTE is really better to store it?
        self.parent = parent

    # NOTE implement a copy (as a deep one) is very costly
    def copy_like(self):
        return Node(state = self.state.copy(),
                    origin_move = self.origin_move,
                    children = None,
                    wins = 0,
                    draws = 0,
                    visits = 0,
                    parent = self.parent)

    def add_child(self, node):
        self.children.append(node)

    def add_parent(self, node):
        self.parent = node

    def get_move(self):
        if len(self.untried_moves) == 0:
            return (-1, -1) # pass move
        else:
            move = self.untried_moves.pop()
            return move

    def game_ended(self):
        return self.state.game_ended

    def all_possible_moves(self):
        return self.state.all_possible_moves()

    # NOTE older version
    # def do_random_move(self):
    #     move = self.get_move()
    #     debug('trying to play at ' + conv_int_to_letters(move))
    #     valid_action = self.state.process_move(move)
    #     self.print_board()
    #     self.print_liberties()
    #     if not valid_action:
    #         raise Exception('not a valid move', conv_int_to_letters(move))
    #     self.origin_move = move
    #     self.children = []
    #     self.wins = 0
    #     self.draws = 0
    #     self.visits = 0

    def do_random_move(self):
        move = self.state.do_random_move()
        self.origin_move = move
        self.children = []
        self.wins = 0
        self.draws = 0
        self.visits = 0

    def print_board(self):
        return self.state.print_board()

    def print_liberties(self):
        return self.state.print_liberties()

    def update_statistics(self, winner):
        if winner == self.state.current_player:
            self.wins += 1
        elif winner == 0:
            self.draws += 1
        self.visits += 1

    def get_winner(self):
        return self.state.get_winner()

    def get_game_length(self):
        return self.state.game_length

    def get_win_rate(self):
        return self.wins / self.visits

    def ucb(self, c):
        return self.wins / self.visits + c * math.sqrt(2 * math.log(self.parent.visits) / self.visits)

class MCTSPlayer:
    def __init__(self, size = 19, color = 1, max_iter = 1, reuse_subtree = True, tree_policy = 'uct', root = None, max_game_length = None, exploration_constant = 0.5):
        # NOTE this player uses chinese rules
        # NOTE cannot play handicap games yet
        self.size = size
        self.color = color
        self.max_iter = max_iter
        self.reuse_subtree = reuse_subtree
        self.tree_policy = tree_policy
        self.root_node = Node(state = GameState(n = self.size)) if root == None else root
        self.policies = {
                        'uct' : self.uct,
                        'policy_network' : self.policy_network
                        }
        # self.max_game_length = self.size*self.size if max_game_length == None else max_game_length
        self.max_game_length = 10 if max_game_length == None else max_game_length
        self.exploration_constant = exploration_constant

    def append_node(self, parent, child):
        parent.add_child(child)
        child.add_parent(parent)

    def uct_select_child(self, node): # TODO this is wrong. put uct real function
        shuffle(self.root_node.children) # NOTE here it seems necesssary
        selected_node = None
        best_ucb = -1
        for nd in node.children:
            ucb = nd.ucb(self.exploration_constant)
            if ucb > best_ucb:
                selected_node = nd
                best_ucb = ucb
        return selected_node

    def uct(self):
        root_node = self.root_node

        for i in range(self.max_iter):
            debug('#######################################')
            debug('Iterarion ' + str(i) + ':')
            debug('#######################################')
            # Selection
            debug('---------------------------------------')
            debug('Selection')
            debug('---------------------------------------')
            current = root_node
            while not current.game_ended() and len(current.untried_moves) == 0:
                current = self.uct_select_child(current)
            # Expansion
            debug('---------------------------------------')
            debug('Expansion')
            debug('---------------------------------------')
            if not current.game_ended() and len(current.untried_moves) > 0:
                # move = current.get_move()
                # print 'move', conv_int_to_letters(move)
                node = current.copy_like()
                print 'untried moves'
                print node.untried_moves
                node.do_random_move()
                self.append_node(current, node) # current.add_child(node) + something
                current = node
            else:
                # NOTE there is a chance that the algorithm will always come back here?
                pass
            # Simulation
            debug('---------------------------------------')
            debug('Simulation')
            debug('---------------------------------------')
            debug('Board before simulation')
            current.print_board() # debug
            current.print_liberties()
            node = current.copy_like()
            num_steps = 0
            while not node.game_ended() and node.get_game_length() < self.max_game_length:
                num_steps += 1
                print 'step', num_steps
                print 'possible moves'
                print node.state.all_possible_moves()
                node.do_random_move()
            # Backpropagation
            debug('---------------------------------------')
            debug('Backpropagation')
            debug('---------------------------------------')
            winner = node.get_winner()
            while current != None:
                current.update_statistics(winner)
                current = current.parent

        selected_node = self.get_best_node()
        return selected_node.origin_move

    def policy_network(self):
        pass

    def gen_move(self):
        heuristic = self.policies[self.tree_policy]
        return heuristic()

    def get_best_node(self):
        shuffle(self.root_node.children) # NOTE to avoid give preference to left most. is it necessary?
        selected_node = None
        best_win_rate = -1
        for nd in self.root_node.children:
            if nd.visits == 0:
                break
            win_rate = nd.wins / nd.visits # to make it float division
            if win_rate > best_win_rate:
                selected_node = nd
                best_win_rate = win_rate
        return selected_node

class HumanPlayer:
    def __init__(self):
        self.state = GameState(n = 19)

    def gen_move(self): # TODO handle invalid moves!
        is_legal_move = False
        while not is_legal_move:
            stdin = raw_input('Please enter a valid move \n')
            x, y = conv_letter_to_int(stdin)
            is_legal_move = self.state.legal_move(x, y)
        # TODO process move in self.state
        return (x, y)

    def process_move(self, move):
        self.state.process_move(move)

class Game:
    def __init__(self, player1, player2, n = 19):
        self.players = {1 : player1, -1 : player2}
        self.state = GameState(n = 19)

    def play_match(self):
        while not self.state.game_ended:
            self.state.print_board()
            move = self.players[self.state.current_player].gen_move()
            self.state.process_move(move)
            for i in self.players:
                self.players[i].process_move(move)