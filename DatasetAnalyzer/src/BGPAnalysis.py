'''
Created on Jul 7, 2014

@author: lkastler
'''
import re
import Config as config

def removeList(string):
	return re.sub('^\[', "", re.sub('\]$', '', string))

def removeSet(string):
	return re.sub('^\(', "", re.sub('\)$', '', string))

def splitLists(string):
	return removeSet(string).split('), (')

if __name__ == '__main__':
	print 'start'
	
	regex = re.compile('\[.*\]')
	
	f = open (config.bgpfile, 'r')
	o = open (config.bgpanalysisLog, 'w+')
	o.write('Triples\tVariables\n')
	for line in f.readlines():
		
		
		
		outer_list = removeList(line)
		inner_list = outer_list.split(', set')
		
		o.write(str(len(splitLists(removeList(inner_list[0])))) + ', ' + str(len(removeList(removeSet(inner_list[1])).split(", "))) + '\n')
		
	f.close()
	o.close()
	print 'end'