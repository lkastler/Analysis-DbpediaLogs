'''
Created on Jun 25, 2014

@author: lkastler
'''

import Config as config
from dbpedia_analyzer import Extractor as ex
from dbpedia_analyzer import FileParser as fp
import logging as log
import sys
	
def main():
	'''teh main'''
	log.basicConfig(filename=config.extractionLog,level=log.DEBUG)
	
	logger = log.getLogger("main")
	
	logger.info("START")
	
	malsparql = open(config.malformedsparql, 'w+')
	sparqls = open(config.sparqloutput, 'w+')
	
	extract = ex.Extractor(logger, sparqls, malsparql)
	
	for f in fp.parseFolder(logger, config.inputfolder):
		for item in fp.parseBZ2File(logger, f):
			extract.extract(item)
		logger.info(extract.stats)
		
	sparqls.flush()
	sparqls.close()
	
	malsparql.flush()
	malsparql.close()
	
	logger.info("END")
	logger.info(extract.stats)
	
	return 0

if __name__ == '__main__':
	status = main()
	sys.exit(status)