'''
Created on Jul 2, 2014

@author: lkastler
'''

import apachelog
import rdflib.plugins.sparql as validator
import re
import urllib2
from collections import defaultdict
		
class Extractor:
	''' extracts urls and sparql queries from dbpedia server log files and tracks information about the data.'''
	
	'''general purpose apache log file structure'''
	_log_format = r'%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\"'
	
	'''identifies the primary resource'''
	_primary_resource = re.compile('^/\w+(\?|/)?')
	
	def __init__(self, logger, sparqls, malformed):
		'''initial set up'''
		# logging
		self.log = logger
		
		# stats
		self.stats = defaultdict(int)
		
		# files
		self.sparqls = sparqls
		self.malformed = malformed
		
		# apache log file parser
		self.parser = apachelog.parser(Extractor._log_format)
		
		self.log.info("created extractor")
	
	
	def extract(self, line):
		''' starts the extraction process for one line encoding a Apache log file entry '''
		self.stats['count'] += 1
		
		self.extractResource(line)
	
	def extractResource(self, line):
		''' extracts the resource from a apache log file '''
		res = self.parser.parse(line)
		self.analyzeResource(res['%r'])
		
	
	
	def analyzeResource(self, res):
		''' tests regex pattern on the given url snipplet and executes corresponding functions if they match '''
		primRes = Extractor._primary_resource.match(res)
		
		if  primRes != None:
			identifier = re.sub('(\?|/)', '', primRes.group(0))
			
			if identifier != None:
				self.stats[identifier] += 1
				
				# handle sparql differentyl
				if identifier == "sparql":
					self.extractSparql(res)
		else:
			self.log.warn("could not identify kind of request", res)
	
	
	def extractSparql(self, res):
		''' extracts sparql query from the given resource snipplet ''' 
		request = re.sub("/sparql\?", '', res)
		req_split = request.split('&')
		
		for param in req_split:
			if re.match('^query', param) != None:
				query = re.sub('^query=', '', param)
				query = urllib2.unquote(query)
				query = re.sub('(\+)+', ' ', query)
				query = re.sub('\s+', ' ', query)
				query = query.strip()
				
				self.validateSparql(query)
	
	
	def validateSparql(self, sparql):
		''' validates a sparql query and stores it in a separate file '''
		sparql = str(sparql)
		
		try:
			validator.prepareQuery(sparql)
			self.sparqls.write(sparql + '\n')
		except Exception as error:
			self.stats['malformed-sparql'] += 1 
			self.malformed.write(str([str(type(error)), str(error), sparql]) + '\n')