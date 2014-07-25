'''
Created on Jul 23, 2014

@author: lkastler
'''

import rdflib.plugins.sparql as sparql

class MalformedSparqlQueryError(Exception):pass

class SparqlValidator(object):
	'''
	validates SPARQL queries
	'''
	def __init__(self, namespaces={}):
		'''
		Constructor
		'''
		self.namespaces = namespaces
		
	def validateSparql(self, text):
		''' validates a sparql query and stores it in a separate file '''
		text = str(text)
		
		try:
			return sparql.prepareQuery(text, initNs=self.namespaces)
		except Exception as error: 
			raise MalformedSparqlQueryError([str(type(error)), str(error), sparql])