def debug(s):
    print s

def conv_int_to_letters(move):
    if move == (-1, -1):
        return 'pass'
    s = 'abcdefghijklmnopqrstuvwxyz'
    return s[move[0]]+ s[move[1]]

def conv_letter_to_int(move):
    s = 'abcdefghijklmnopqrstuvwxyz'
    return (s.index(move[0]), s.index(move[1]))

def player_num_to_symbol(player):
    if player == 1:
        return 'x'
    elif player == 0:
        return '.'
    elif player == -1:
        return 'o'
    else:
        raise Exception('not a valid number for stone', player)
