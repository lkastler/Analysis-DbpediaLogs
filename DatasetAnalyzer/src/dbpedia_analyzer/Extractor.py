'''
Created on Jul 2, 2014

@author: lkastler
'''

import re
import urllib2
from collections import defaultdict
import apachelog
from apachelog import ApacheLogParserError
	
class Extractor:
	''' extracts urls and sparql queries from dbpedia server log files and tracks information about the data.'''
	
	''' general purpose apache log file structure '''
	_log_format = r'%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\"'
	
	'''identifies the primary resource'''
	_primary_resource = re.compile('^/\w+(\?|/)?')
	
	def __init__(self, logger, sparqlFile):
		''' initial set up '''
		# logging
		self.log = logger
		# stats
		self.stats = defaultdict(int)
		# files
		self.sparqlFile = sparqlFile
		
		# apache log file parser
		self.parser = apachelog.parser(Extractor._log_format)
		
		self.log.info("created extractor")
	
	def extract(self, line):
		''' starts the extraction process for one line encoding a Apache log file entry '''
		self.stats['count'] += 1
		
		return self.extractResource(line)
	
	def extractResource(self, line):
		''' extracts the resource from a apache log file '''
		resource = None
		try:
			res = self.parser.parse(line)
			resource = res['%r']
			
		except ApacheLogParserError as e:
			lines = line.split('"')
			#self.log.warn(str(e))
			
			if lines != None and len(lines) >= 2:
				self.log.debug(lines)
				lines = lines[1].split(" ")
				if lines != None and len(lines) >= 2:
					self.log.debug(lines)
					resource = str(lines[1])
					self.log.debug(resource)
			
		return self.analyzeResource(resource)
	
	def analyzeResource(self, res):
		''' tests regex pattern on the given url snipplet and executes corresponding functions if they match '''
		primRes = Extractor._primary_resource.match(res)
		
		if  primRes != None:
			identifier = re.sub('(\?|/)', '', primRes.group(0))
			
			if identifier != None:
				self.stats[identifier] += 1
				
				
				# handle sparql differently
				if identifier == "sparql":
					return self.extractSparql(res)
		else:
			self.log.warn(["could not identify kind of request", res])
	
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
				return query.strip()
	