import shutil
import os
import subprocess
from subprocess import call

# ---------------------------------------------------------------------- #
# Step 1: Use Qsub in all of the jobs

# get the cwd
cwd=os.getcwd()

# get the directories and their names
allFiles=os.listdir(cwd)
allDirs=[]
for i in allFiles:
	if '.' not in i:
		allDirs.append(i)

# move the cwd into each of the molecules
for i in allDirs:
	cwd=cwd+'/'+i

	# extract the directories from each of these directories
	loopFiles=os.listdir(cwd)
	loopDirs=[]
	for j in loopFiles:
		if '.' not in j:
			loopDirs.append(j)

	# for each of the "loopDirs", go in and execute the csvE function
	for k in loopDirs:
		# call(["ls", "-l"],cwd=cwd+'/'+k)
		call(["qsub","runAll.sch"],cwd=cwd+'/'+k)

	cwd=os.getcwd()
