'''
Created on Jun 25, 2014

@author: lkastler
'''

if __name__ == '__main__':
	import Config as config
	from dbpedia_analyzer import Extractor as ex
	from dbpedia_analyzer import FileParser as fp
	import logging
	logging.basicConfig(filename=config.extractionLog,level=logging.DEBUG)
	
	logger = logging.getLogger("main")
	malsparql = open(config.malformedsparql, 'w+')
	sparqls = open(config.sparqloutput, 'w+')
	extract = ex.Extractor(logger, sparqls, malsparql)
	try:
		for f in fp.parseFolder(logger, config.inputfolder):
			for item in fp.parseFile(logger, f):
				extract.extract(item)
	except Exception as ex:
		logger.error("Exception: ", ex)
	finally:
		sparqls.flush()
		sparqls.close()
		
		malsparql.flush()
		malsparql.close()
		
		logger.info(extract.stats)