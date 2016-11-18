# helpful functions
def letter_to_num(c):
	return ord(c) - 97

def pos_to_array_in_file(pair, f, n = 19):
    for i in range(n):
        for j in range(n):
            if i == pair[0] and j == pair[1]:
                f.write('1')
            else:
                f.write('0')
            if i + j != 2*n - 2:
                f.write(' ')

def write_header(f):
        columns = ['player_stones',
                    'opponent_stones',
                    'empty_intersections',
                    'ones',
                    'turns_since_1',
                    'turns_since_2',
                    'turns_since_3',
                    'turns_since_4',
                    'turns_since_5',
                    'turns_since_6',
                    'turns_since_7',
                    'turns_since_8',
                    'liberties_1',
                    'liberties_2',
                    'liberties_3',
                    'liberties_4',
                    'liberties_5',
                    'liberties_6',
                    'liberties_7',
                    'liberties_8',
                    'capture_size_1',
                    'capture_size_2',
                    'capture_size_3',
                    'capture_size_4',
                    'capture_size_5',
                    'capture_size_6',
                    'capture_size_7',
                    'capture_size_8',
                    'self_atari_size_1',
                    'self_atari_size_2',
                    'self_atari_size_3',
                    'self_atari_size_4',
                    'self_atari_size_5',
                    'self_atari_size_6',
                    'self_atari_size_7',
                    'self_atari_size_8',
                    'liberties_after_move_1',
                    'liberties_after_move_2',
                    'liberties_after_move_3',
                    'liberties_after_move_4',
                    'liberties_after_move_5',
                    'liberties_after_move_6',
                    'liberties_after_move_7',
                    'liberties_after_move_8',
                    'zeros',
                    'move']
        m = len(columns)
        for i in range(m):
            f.write(columns[i])
            if i == m - 1:
                f.write('\n')
            else:
                f.write(',')

def coord_to_pos(x, y, n = 19):
    return x * n + y
