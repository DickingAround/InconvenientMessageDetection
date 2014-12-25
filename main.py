#Just change the coding
#Put a bunch of files in an archive and change them
#Build it into an image

def codeByte(byte,encoding):
	return chr(ord(byte)^encoding)
def codeName(oldName):
	newName = ''
	for c in oldName:
		newName += c + 'a'
	return newName
def uncodeName(newName):
	oldName = ''
	for i in range(len(newName)):
		if(i % 2 == 0):
			oldName += newName[i]
	return oldName
def code(fileName,encoding,dOrE):
	try:
		if(dOrE == 'd'):
			newName = uncodeName(fileName)
		else:
			newName = codeName(fileName)
		fi = open(fileName,'rb')
		fo = open(newName,'wb')
		byte = fi.read(1)
		while byte != "":
			print byte+'"'+codeByte(byte[0],encoding)+'"'+codeByte(codeByte(byte[0],encoding),encoding)
			fo.write(codeByte(byte[0],encoding))
			byte = fi.read(1)
	finally:
		fi.close()
		fo.close()

if __name__ == '__main__':
	import sys
	co = int(sys.argv[2])
	if(co > 255 or co < 0):
		print "Bad code"
		sys.exit(0)
	if((len(sys.argv) == 4) and sys.argv[3] == 'd'):
		code(sys.argv[1],co,'d')
	code(sys.argv[1],co,'e')

