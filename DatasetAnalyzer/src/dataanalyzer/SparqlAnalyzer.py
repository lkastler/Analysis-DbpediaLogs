'''
Created on Jul 2, 2014

@author: lkastler
'''

''''''
def extractURL(line):
	request = line.split('"')[1]
	request = request.split(' ')[1]
	return request

''''''
def analyzeQuery(sparql):
	from dataanalyzer import Stats as s
	
	s.stats['sparql'] += 1

''''''
def extractSparql(url): 
	import urllib2
	import re
	
	request = re.sub("/sparql\?", '', url)
	request = request.split('&')[0]
	
	if re.match('^query', request) != None:
		request = re.sub('^query=', '', request)
		request = urllib2.unquote(request)
		request = re.sub('(\+)+', ' ', request)
		request = re.sub('\s+', ' ', request)
		request = request.strip()
		analyzeQuery(request)

def handleResource(url):
	from dataanalyzer import Stats as s
	s.stats["resource"] += 1

def handleOntology(url):
	from dataanalyzer import Stats as s
	s.stats['ontology'] += 1

def analyze(url):
	import re
	from dataanalyzer import Stats as s
	patterns = dict()
	patterns[re.compile('^/sparql')] = extractSparql
	patterns[re.compile('^(/resource|/page)')] = handleResource
	patterns[re.compile ('^/ontology')] = handleOntology
	
	for pattern, func in patterns.iteritems():
		if pattern.match(url) != None:
			func(url)
		s.stats['queries'] += 1