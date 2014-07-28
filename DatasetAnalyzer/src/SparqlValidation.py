'''
Created on Jul 28, 2014

@author: lkastler
'''
import cProfile
import Config as config
from dbpedia_analyzer import FileParser as fp
import logging as log
from dbpedia_analyzer import SparqlValidator as valid 
from dbpedia_analyzer.SparqlValidator import MalformedSparqlQueryError

def validate():
	log.basicConfig(level=log.DEBUG)
	
	log.info("start")
	
	validator = valid.SparqlValidator()
	
	f = open(config.validSparql, "w+")
	
	for line in fp.parseFile(log.getLogger("Validator"),config.sparqlFile):
		try:
			validator.validateSparql(line)
			f.write(line)
		except MalformedSparqlQueryError as e:
			log.warn(str(e))
	f.close()
	
	log.info('end')

if __name__ == '__main__':
	cProfile.run("validate()")