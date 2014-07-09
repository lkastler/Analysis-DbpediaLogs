'''
Created on Jul 2, 2014

@author: lkastler
'''
class Extractor:
	''''''
	def __init__(self, logger, sparqls, malformed):
		import re
		self.logger = logger
		
		self.stats = {}
		self.stats['count'] = 0
		self.stats['resource'] = 0
		self.stats['ontology'] = 0
		self.stats['malformed-sparql'] = 0
		self.stats['sparql'] = 0
		
		self.patterns = dict()
		self.patterns[re.compile('^/sparql')] = self.extractSparql
		self.patterns[re.compile('^/(resource|page)')] = self.handleResource
		self.patterns[re.compile ('^/ontology')] = self.handleOntology
		
		self.sparqls = sparqls
		self.malformed = malformed
		self.logger.info("created extractor")
	
	''''''
	def extract(self, line):
		self.stats['count'] += 1
		self.analyzeUrl(self.extractUrl(line))
	
	''''''
	def extractUrl(self, line):
		request = line.split('"')[1]
		request = request.split(' ')[1]
		return request
	
		''''''
	def analyzeUrl(self, url):
		for pattern, func in self.patterns.iteritems():
			if pattern.match(url) != None:
				func(url)
	
	''''''
	def extractSparql(self, url): 
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
			
			self.validateSparql(request)
	
	''''''
	def validateSparql(self, sparql):
		import rdflib.plugins.sparql as validator
		
		sparql = str(sparql)
		
		try:
			validator.prepareQuery(sparql)
			self.stats['sparql'] += 1
			self.sparqls.write(sparql + '\n')
			
		except Exception as error:
			self.stats['malformed-sparql'] += 1 
			self.malformed.write(str([str(type(error)), str(error), sparql]) + '\n')
	
	def handleResource(self, url):
		self.stats["resource"] += 1
	
	def handleOntology(self, url):
		self.stats['ontology'] += 1
	
	