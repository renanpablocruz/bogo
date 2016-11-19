def debug(s):
    print s

def conv_int_to_letters(move):
    x, y = move
    s = 'abcdefghijklmnopqrstuvwxyz'
    return s[x]+ s[y]