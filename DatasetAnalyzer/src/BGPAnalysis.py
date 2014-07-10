'''
Created on Jul 7, 2014

@author: lkastler
'''
import re
import Config as config
import logging
logging.basicConfig(filename=config.bgpanalysisLog,level=logging.DEBUG)

def removeList(string):
	return re.sub('^\[', "", re.sub('\]$', '', string))

def removeSet(string):
	return re.sub('^\(', "", re.sub('\)$', '', string))

def splitLists(string):
	return removeSet(string).split('), (')

if __name__ == '__main__':
	logging.info('start')
	
	regex = re.compile('\[.*\]')

	f = open (config.bgpfile, 'r')
	o = open (config.bgpanalysis, 'w+')
	
	o.write('Triples\tVariables\n')
	
	for line in f.readlines():
		try:
			outer_list = removeList(line)
			inner_list = outer_list.split(', set')
			
			o.write(str(len(splitLists(removeList(inner_list[0])))) + ', ' + str(len(removeList(removeSet(inner_list[1])).split(", "))) + '\n')
		except Exception as e:
			logging.error("Error: " + e)
		
	f.close()
	o.close()
	logging.info('end')