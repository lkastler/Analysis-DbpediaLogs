'''
Created on Jun 25, 2014

@author: lkastler
'''



if __name__ == '__main__':
	from dataanalyzer import Stats as stats
	from dataanalyzer import FileParser as fp	
	from dataanalyzer import SparqlAnalyzer as sa
	
	print "processing"
	
	for f in fp.parseFolder('test'):
		for item in fp.parseFile(f):
			sa.analyze(sa.extractURL(item))
	print "done"
	
	print stats.stats