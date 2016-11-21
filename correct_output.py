# transform y array to single number
import os

path = os.getcwd()

def pos_of_one(l):
    pos = -1
    l = l.split(' ')
    for i in range(len(l)):
        if l[i] == '1':
            pos = i
            break
    return str(pos)

for fname in sorted(os.listdir(path)):
    if fname.endswith('.csv'):
        fin = path + '/' + fname
        fout = path + '/' + fname.split('.')[0] + '.data'
        with open(fin, 'r') as f:
            with open(fout, 'w') as g:
                g.write(f.readline()) # header
                for line in f:
                    l = line.strip().split(',')
                    l[-1] = pos_of_one(l[-1])
                    g.write(','.join(l) + '\n')
