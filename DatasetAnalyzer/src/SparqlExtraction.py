'''
Created on Jun 25, 2014

@author: lkastler
'''
import cProfile
import Config as config
from dbpedia_analyzer import Extractor as ex
from dbpedia_analyzer import FileParser as fp
import logging as log
import sys
import traceback

def main():
	'''teh main'''
	log.basicConfig(filename=config.extractionLog,level=log.DEBUG)
	
	logger = log.getLogger("main")
	
	logger.info("START")
	
	sparqls = open(config.sparqlLogEntries, 'w+')
	
	extract = ex.Extractor(logger, sparqls)
	
	for f in fp.parseFolder(logger, config.inputfolder):
		for item in fp.parseBZ2File(logger, f):
			try:
				query = extract.extract(item)
				
				if query != None:
					sparqls.write(query + '\n')
			except Exception:
				exc_type, exc_value, exc_traceback = sys.exc_info()
				lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
				logger.error(''.join(line for line in lines))
		logger.info(extract.stats)
		
	sparqls.flush()
	sparqls.close()
	
	logger.info("END")
	logger.info(extract.stats)
	
	return 0

if __name__ == '__main__':
	cProfile.run("main()")