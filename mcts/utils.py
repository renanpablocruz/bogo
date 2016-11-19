def debug(s):
    print s

def conv_int_to_letters(move):
    if move == (-1, -1):
        return 'pass'
    s = 'abcdefghijklmnopqrstuvwxyz'
    return s[move[0]]+ s[move[1]]