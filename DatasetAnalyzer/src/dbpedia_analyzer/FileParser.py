''' parses all files in the given folder '''
def parseFolder(logger, folderName):
	import os
	
	logger.info("processing folder: %s", folderName)
	
	for dirname, _, filenames in os.walk(folderName):
		for filename in filenames:
			yield os.path.join(dirname,filename)
			
	logger.info('done')


''' parses given bz2 file'''
def parseFile(logger, fileName):
	import bz2  # @UnresolvedImport
	
	logger.info('loading file: %s', fileName)
	
	f = bz2.BZ2File(fileName)
	
	for line in f.readlines():
		yield line
	logger.info('done loading file')
	f.close()