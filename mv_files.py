from subprocess import call

for i in range(20):
	folder = "games_" + str(i)
	call(["mkdir", folder])
	size = 20
	for j in range(size):
		fname = str(20080 + size*i + j) + '.sgf'
		call(["cp", "game_records/" + fname, folder + "/" + fname])
		call(["cp", "convert_dataset.py", folder + "/" + "convert_dataset.py"])
