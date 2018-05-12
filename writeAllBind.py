#! /usr/bin/env python
# Import shell libraries
import shutil
import os

def write(cwd,name):

	structure=cwd[cwd.rfind('/')+1:]
	allFiles=os.listdir(cwd)
	startFile=[]
	for i in allFiles:
		if 'startingPoint.com' in i:
			startFile=i

	# find all the files and remove existing .com files
	allFiles=os.listdir(cwd)
	for i in allFiles:
		if 'startingPoint.com' in i:
			a=1
		elif '.py' in i:
			a=1
		elif '.log' in i:
			a=1
		else:
			os.remove(cwd+'/'+i)

	# make the starting point a text file, open it, and read it
	txtStart=startFile[:-4]+'.txt'
	shutil.copyfile(cwd+'/'+startFile,cwd+'/'+txtStart)

	startingPoint=open(cwd+'/'+txtStart,'r')
	inputList=startingPoint.readlines()


	# create a list for all the files you want to create
	methodNames=['HF','PBEPBE','B3LYP']
	basisNames=['STO3G','631Gd','631Gdp','631+Gdp','631++Gdp','6311++Gdp']
	comFiles=[['' for i in range(len(basisNames))] for j in range(len(methodNames))]
	for i in range(len(methodNames)):
		for j in range(len(basisNames)):
			comFiles[i][j]=(methodNames[i]+'_'+basisNames[j]+'.com')

	# write the .com stuff (input titles, multiplicity, and charge)
	description='Clay System Binding'
	multiplicity=1
	if structure=='anion':
		charge=-1
		tests=['SP']
	elif structure=='cation':
		charge=1
		tests=['SP']
	else:
		charge=0
		tests=['Opt']

	methods=['HF','PBEPBE','B3LYP']
	basis=['STO-3G','6-31G(d)','6-31G(d,p)','6-31+G(d,p)','6-31++G(d,p)','6-311++G(d,p)']
	for i in range(len(methods)):
		for j in range(len(basis)):
			output=open(cwd+'/'+comFiles[i][j], 'w+')

			output.write('%NProcShared=12\n')
			output.write('LindaWorker=localhost\n')
			output.write('#n %s/'% methods[i])
			output.write('%s ' % basis[j])
			for m in range(len(tests)):
				output.write('%s ' % tests[m])
			output.write('\n')
			output.write('\n')
			output.write(' %s ' % description)
			output.write('%s/' % methods[i])
			output.write('%s \n' % basis[j])
			output.write('\n')
			output.write('%d ' % charge)
			output.write('%d\n' % multiplicity)
			for k in range(len(inputList)):
				if k>4:
					output.write(inputList[k])

	# write the .sch file (edit the title, and description here)

	title=name
	output=open(cwd+'/'+'runAll.sch', 'w+')

	output.write('#!/bin/csh\n')
	output.write('# %s\n' % description)
	output.write('#$ -N %s\n' % title)
	output.write('#$ -q long\n')
	output.write('#$ -pe smp 12\n')
	output.write('#$ -M celmore1@nd.edu\n')
	output.write('#$ -m ae\n')
	output.write('#$ -r n\n\n')
	output.write('module load gaussian\n\n')
	for i in range(len(methodNames)):
		for j in range(len(basisNames)):
			output.write('g09 '+methodNames[i]+'_'+basisNames[j]+'.com\n\n')

	# remove the .txt file for the starting point for clutter issues
	os.remove(cwd+'/'+'startingPoint.txt')




# ---------------------------------------------------------------------- #
# Step 1: Run the writing function in all the directories 

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
		name=i+'_'+k
		write(cwd+'/'+k,name)
		print(name)

	cwd=os.getcwd()
