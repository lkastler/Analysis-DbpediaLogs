'''
Created on Jun 25, 2014

@author: lkastler
'''

if __name__ == '__main__':
	import Config as config
	import logging
	logging.basicConfig(filename=config.extractionLog,level=logging.DEBUG)
	
	logger = logging.getLogger(__name__)
	
	malsparql = open(config.malformedsparql, 'w+')
	sparqls = open(config.sparqloutput, 'w+')
	
	from dbpedia_analyzer import FileParser as fp	
	from dbpedia_analyzer import Extractor as ex
	
	extract = ex.Extractor(logger, sparqls, malsparql)
	
	for f in fp.parseFolder(logger, config.inputfolder):
		for item in fp.parseFile(logger, f):
			extract.extract(item)
	
	sparqls.flush()
	sparqls.close()
	
	malsparql.flush()
	malsparql.close()
	
	logger.info(extract.stats)