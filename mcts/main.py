from mcts import MCTSPlayer

mcts = MCTSPlayer(size = 3)
move = mcts.gen_move()

print 'chosen move is', move
