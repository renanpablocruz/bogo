# # remove duplicate numbers in a file
# import os

# folder = os.getcwd()

# with open(folder + '/' + 'game_records/files_with_problems.txt', 'r') as f:
#     with open(folder + '/' + 'game_records/problems.txt', 'w') as g:
#         nums = set([])
#         for line in f:
#             n = line.strip()
#             if n not in nums:
#                 g.write(n + '\n')
#                 nums.add(n)

# mv files to other folder
import os
from subprocess import call

folder = os.getcwd()

with open(folder + '/' + 'game_records/problems.txt', 'r') as f:
    for line in f:
        n = line.strip()
        fname = n + '.sgf'
        # print fname
        call(["mv", folder + "/game_records/" + fname, folder + "/games_with_problems/" + fname])
        # break
