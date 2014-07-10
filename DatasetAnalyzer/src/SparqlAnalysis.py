'''
Created on Jul 7, 2014

@author: lkastler
'''
import Config as config
import re
import logging
import rdflib.plugins.sparql as sparql

logging.basicConfig(filename=config.analysisLog,level=logging.DEBUG)

''''''
def handleUnion(regex, query):
	countKeywords('union', regex, query)

''''''
def handleSelect(regex, query):
	countKeywords('select', regex, query)

''''''
def handleOptional(regex, query):
	countKeywords('optional', regex, query)

''''''
def handleGraph(regex, query):
	countKeywords('graph', regex, query)

''''''
def handleDescribe(regex, query):
	countKeywords('describe', regex, query)

''''''
def handleAsk(regex, query):
	countKeywords('ask', regex, query)

''''''
def handleFilter(regex, query):
	countKeywords('filter', regex, query)

def countKeywords(keyword, regex, query):
	global result
	
	count = str(len(regex.findall(query)))
	if count not in result[keyword]: 
		result[keyword][count] = 0
	result[keyword][count] += 1

def getBGP(f, query):
		try:
			sq = sparql.prepareQuery(query)
		except Exception as error:
			logging.warn(str([str(type(error)), str(error), sparql]) + '\n')
			return
			
		if sq.algebra.name == "SelectQuery":
			if sq.algebra.p.name == 'Project':
				if sq.algebra.p.p.name == 'BGP':
					f.write(str([sq.algebra.p.p.triples, sq.algebra.p.p._vars]) + '\n')
			
		del sq
	

''''''''
def startAnalysis():
	logging.info('begin')
	
	regexs = dict()
	regexs[re.compile('\s+(union|UNION)\s+')] = handleUnion 
	regexs[re.compile('\s+(select|SELECT)\s+')] = handleSelect 
	regexs[re.compile('\s+(optional|OPTIONAL)\s+')] = handleOptional 
	regexs[re.compile('\w(ask|ASK)\w')] = handleAsk 
	regexs[re.compile('\w(describe|DESCRIBE)\w')] = handleDescribe
	regexs[re.compile('\w(graph|GRAPH)\w')] = handleGraph
	regexs[re.compile('\w(filter|FILTER)\w')] = handleFilter
	
	try:
		bgp = open(config.bgpfile, 'w+')
		sparqls = open(config.sparqloutput, "r")
	except Exception as e:
		logging.error("Error: ", e)
	
	logging.info('parse: ' + config.sparqloutput)
	
	result = {'queries': 0}
	
	for key in regexs:
			result[str(key)] = {}
	try:
		for line in sparqls.readlines():
			result['queries'] += 1		
				
			for regex, func in regexs.iteritems():
				if regex.match(line):
					func(regex, line)
			
			getBGP(bgp, str(line))
	except Exception as e:
		logging.error("Error: ", e)
	finally:
		bgp.flush()
		bgp.close()
		
		sparqls.flush()
		sparqls.close()
		
		logging.info(result)
	
if __name__ == '__main__':
	startAnalysis()