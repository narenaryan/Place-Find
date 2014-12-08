cats= []
with open('NationalFile_20141005.txt','r') as fil:
	for i in fil.readlines():
		cats.append((i.rstrip().split('|'))[2])

#List the places and take input from User for Park,Bar,Hotel etc
#we can use dict(enumerate(set(cats))) here but we need to delete FEATURE_CLASS,Unknown fields from list
show_first = {k:v for k,v in enumerate(set(cats)) if v != 'FEATURE_CLASS' and v != 'Unknown'} 