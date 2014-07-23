'''
Created on Jul 7, 2014

@author: lkastler
'''
from collections import defaultdict
import Config as config
from dbpedia_analyzer import FileParser as FP 
import logging as log
import namespaces as ns
import rdflib.plugins.sparql as sparql
import re
import sys

results = defaultdict(int)

def handleSelect(regex, query):
	countKeywords('select', regex, query)

def handleGraph(regex, query):
	countKeywords('graph', regex, query)

def handleDescribe(regex, query):
	countKeywords('describe', regex, query)

def handleAsk(regex, query):
	countKeywords('ask', regex, query)

def handleUnion(regex, query):
	countKeywords('union', regex, query)

def handleOptional(regex, query):
	countKeywords('optional', regex, query)

def handleFilter(regex, query):
	countKeywords('filter', regex, query)

def countKeywords(keyword, regex, query):
	''' counts the occurrences of given keyword in the given query by using the given regular expression'''
	count = str(len(regex.findall(query)))
	
	global resultsimport
	
	if keyword not in results:
		results[keyword] = defaultdict(int)
	
	results[keyword][count] += 1

def writeOutBGP(f, query):
		''' writes existing BGP statistics (# triples and # of vars) in the query to given file'''
		try:
			sq = sparql.prepareQuery(query, initNs=ns.ns)
		except Exception as error:
			log.warn(str([str(type(error)), str(error), sparql]) + '\n')
			return
			
		# we only look into select queries with a projection
		if sq.algebra.name == "SelectQuery":
			if sq.algebra.p.name == 'Project':
				if sq.algebra.p.p.name == 'BGP':
					f.write(str(len(sq.algebra.p.p.triples)) + ', ' + str(len(sq.algebra.p.p._vars)) + '\n')		
		# will hopefully reduce memory usage
		del sq


def startAnalysis():
	''' starts analyzing '''
	log.basicConfig(filename=config.analysisLog,level=log.DEBUG)
	
	log.info('START')
	
	# list of regular expressions that should be found in the queries
	regexs = {}
	regexs[re.compile('\s+(union|UNION)\s+')] = handleUnion 
	regexs[re.compile('\s+(select|SELECT)\s+')] = handleSelect 
	regexs[re.compile('\s+(optional|OPTIONAL)\s+')] = handleOptional 
	regexs[re.compile('\w(ask|ASK)\w')] = handleAsk 
	regexs[re.compile('\w(describe|DESCRIBE)\w')] = handleDescribe
	regexs[re.compile('\w(graph|GRAPH)\w')] = handleGraph
	regexs[re.compile('\w(filter|FILTER)\w')] = handleFilter
	
	bgp = open(config.bgpfile, 'w+')
	bgp.write("triples, variables\n")
	
	log.info('parse: ' + config.sparqloutput)
	
	global results
	
	#try:
	for line in FP.parseFile(log.getLogger(), config.sparqloutput):
		results['queries'] += 1		
			
		for regex, func in regexs.iteritems():
			if regex.match(line):
				func(regex, line)
		
		writeOutBGP(bgp, str(line))
	#except Exception as e:
	#	logging.error("Error: %s", str(e))
	#finally:
	bgp.flush()
	bgp.close()
	
	log.info("END")
	log.info(results)
	
	return 0
	
'''teh main'''
if __name__ == '__main__':
	status = startAnalysis()
	sys.exit(status)