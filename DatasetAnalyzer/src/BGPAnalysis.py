'''
Created on Jul 7, 2014

@author: lkastler
'''
import re

def removeList(string):
	return re.sub('^\[', "", re.sub('\]$', '', string))

def removeSet(string):
	return re.sub('^\(', "", re.sub('\)$', '', string))

def splitLists(string):
	return removeSet(string).split('), (')

if __name__ == '__main__':
	print 'start'
	
	regex = re.compile('\[.*\]')
	
	f = open ('/home/lkastler/Workspaces/git-repos/DBpediaLogAnalyzer/DatasetAnalyzer/output/bgp.txt')
	
	for line in f.readlines():
		
		print line
		
		outer_list = removeList(line)
		inner_list = outer_list.split(', set')
		
		print len(splitLists(removeList(inner_list[0])))
		print len(removeList(removeSet(inner_list[1])).split(", "))
		
	f.close()
	print 'end'