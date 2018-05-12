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

	# for each of the "loopDirs", go in and take out the core
	for k in loopDirs:
		if k=='neutral':
			coreFiles=os.listdir(cwd+'/'+k)
			for i in coreFiles:
				if ".log" in i:
					fileCheck=open(cwd+'/'+k+'/'+i,'r')
					fileLines=fileCheck.readlines()
					good=False
					for n in fileLines:
						if "Final structure in terms of initial Z-matrix:" in n:
							good=True
						
					if not good:
						print(cwd+'/'+k+'/'+i)

					#os.remove(cwd+'/'+k+'/'+i)
					#print(cwd)

	cwd=os.getcwd()
