'''
Created on Jul 2, 2014

@author: lkastler
'''
class Extractor:
	''' extracts urls and sparql queries from dbpedia server log files and tracks information about the data.'''
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
	
	''' starts the extraction process for one line encoding a Apache log file entry '''
	def extract(self, line):
		self.stats['count'] += 1
		
		self.extractUrl(line)
	
	''' extracts a url from a apache log file '''
	def extractUrl(self, line):
		try:
			request = line.split('"')[1]
			request = request.split(' ')[1]
			
			self.analyzeUrl(request)
		except Exception as error:
			self.logger.info(str([str(type(error)), str(error)]))
	
	''' tests regex pattern on the given url snipplet and executes corresponding functions if they match '''
	def analyzeUrl(self, url):
		for pattern, func in self.patterns.iteritems():
			if pattern.match(url) != None:
				func(url)
	
	''' extracts sparql query from the given url snipplet '''
	def extractSparql(self, url): 
		import urllib2
		import re
		
		request = re.sub("/sparql\?", '', url)
		req_split = request.split('&')
		
		for param in req_split:
			if re.match('^query', param) != None:
				query = re.sub('^query=', '', param)
				query = urllib2.unquote(query)
				query = re.sub('(\+)+', ' ', query)
				query = re.sub('\s+', ' ', query)
				query = query.strip()
				
				self.validateSparql(query)
	
	''' validates a sparql query and stores it in a separate file '''
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
	
	''' analyzes information about the resource request'''
	def handleResource(self, url):
		self.stats["resource"] += 1
	
	''' analyzes information about the ontology request '''
	def handleOntology(self, url):
		self.stats['ontology'] += 1
	
	