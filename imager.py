#Just change the coding
#Put a bunch of files in an archive and change them
#Build it into an image
#len-data
from scipy import misc
#-------Basic tools---------
#Low bits of the byte are at the front of the list
def bitsToByte(bits):
	byte = 0
	for i in range(8):
		byte = byte|(bits[i]<<i)
	return chr(byte)
def byteToBits(b):
	listOfBits = []
	for i in range(8):
		listOfBits.append((ord(b)>>i)&1) 
	return listOfBits
def combineBitAndByte(bit,byte):
	return (byte&254)|(bit&1)
def extractBitFromByte(byte):
	return byte&1
def codeString(s):
	listOfBits = []
	for c in s:
		listOfBits = listOfBits + byteToBits(c)
	return listOfBits

def imageBitIndex(image,index):
	i = int(index/len(image[0]))
	if(i >= len(image)):
		raise Exception("Image file too small")
	j = index%len(image[0])
	k = index%3
	return i,j,k
def extractByteFromImage(image,index):
	bits = []
	for n in range(0,8):
		i,j,k = imageBitIndex(image,index*8+n)
		bits.append(extractBitFromByte(image[i][j][k]))
	return bitsToByte(bits)
def stitchBitsToImage(image,bitData):
	for n in range(0,len(bitData)):
		i,j,k = imageBitIndex(image,n)
		image[i][j][k] = combineBitAndByte(bitData[n],image[i][j][k])

#-------Decode workflow---------
def extractDataStream(image):
	data = []
	fileName = ''
	byteLenghtValue = 0
	#-- Get the length --
	byteLengthString = ''
	currentByte = '-'
	i = 0
	while(currentByte != '*'):	
		currentByte = extractByteFromImage(image,i)
		byteLengthString += currentByte
		i += 1
	byteLengthValue = int(byteLengthString[:len(byteLengthString)-1])
	#-- Get the name --
	currentByte = '-'
	while(currentByte != '*'):	
		currentByte = extractByteFromImage(image,i)
		fileName += currentByte
		i += 1
	fileName = fileName[:len(fileName)-1]
	#-- Get the data --
	for j in range(i,i+byteLengthValue):
		data.append(extractByteFromImage(image,j))
	return fileName,data
def buildFile(fileName,data):
	f = open(fileName,'wb')
	for c in data:
		f.write(c)
	f.close()	

#-------Encode workflow---------
def buildBitList(fileName):
	listOfBits = []
	#fileLength*fileName*bitsOfTheFile
	f = open(fileName,'rb')
	byte = f.read(1)
	bytesRead = 0
	while byte != "":
		bytesRead += 1
		listOfBits += byteToBits(byte)	
		byte = f.read(1)
	f.close()
	listOfBits = codeString(fileName+"*") + listOfBits
	listOfBits = codeString(str(bytesRead)+"*") + listOfBits
	return listOfBits

#-------Main---------
def code(fileName,imageName):
	image = misc.imread(imageName)
	listOfBits = buildBitList(fileName)
	stitchBitsToImage(image,listOfBits)
	misc.imsave('new_'+imageName, image)
def decode(imageName):
	image = misc.imread(imageName)
	fileName,data = extractDataStream(image)
	buildFile(fileName,data)
if __name__ == '__main__':
	import sys
	if(sys.argv[2] == 'd'):
		decode(sys.argv[1])
	else:
		code(sys.argv[1],sys.argv[2])

