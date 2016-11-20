from mcts import MCTSPlayer, HumanPlayer, Game

# mcts = MCTSPlayer(size = 3)
# move = mcts.gen_move()

# print 'chosen move is', move

game = Game(HumanPlayer(), HumanPlayer())
game.play_match()