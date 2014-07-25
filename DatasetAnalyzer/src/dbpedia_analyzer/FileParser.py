import bz2  # @UnresolvedImport
import os

def parseFolder(logger, folderName):
	''' parses all files in the given folder '''
	logger.info("processing folder: %s", folderName)
	
	for dirname, _, filenames in os.walk(folderName):
		for filename in filenames:
			yield os.path.join(dirname,filename)
			
	logger.info('done')

def parseBZ2File(logger, fileName):
	''' parses given bz2 file'''
	logger.info('loading file: %s', fileName)

	f = bz2.BZ2File(fileName)
	line = f.readline()
	
	while line != '':
		yield line
		line = f.readline()
	
	logger.info('done loading file')
	f.close()

def parseFile(logger, fileName):
	''' parses given text file '''
	logger.info('loading file: %s', fileName)
	
	f = open(fileName, 'r')
	
	line = f.readline()
	while line != '' :
		yield line
		line = f.readline()
	
	logger.info('done loading file')
	f.close()