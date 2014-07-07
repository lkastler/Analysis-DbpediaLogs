''' '''
def parseFolder(folderName):
	import os
	for dirname, _, filenames in os.walk(folderName):
		for filename in filenames:
			yield os.path.join(dirname,filename)


''' '''
def parseFile(fileName):
	import bz2  # @UnresolvedImport
	
	print 'loading file: ' + fileName
	
	f = bz2.BZ2File(fileName)
	
	for line in f.readlines():
		yield line
	print 'done loading file'
	f.close()