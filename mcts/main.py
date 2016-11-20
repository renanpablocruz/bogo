from mcts import MCTSPlayer

mcts = MCTSPlayer(size = 5)
move = mcts.gen_move()

print 'chosen move is', move
