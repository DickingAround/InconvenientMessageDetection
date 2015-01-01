#There are three stages to obfuscating: 
#1.	Similar to mining on the bitcoin block chain, build a number (‘X’) is generated from the base image. Then you try many random numbers (‘Y’) until the the result of SHA265(X+Y) has a certain number of 1s (‘N’) at the beginning of it. The user picks N. The larger N they pick, the harder their computer must work doing hashes until the file can be obfuscated into the image (the de-obfuscator will also work harder, as we’ll later see). 
#2.	The number Y is used to seed a pseudo-random number generator. The output of this generator decides where in the image to place the bits of the file being obfuscated. 
#3.	The low-impact bits of the image are changed to ‘1’ or ‘0’ while also checking to make sure a pixel in the image is never written twice, a saturated color is not changed, etc. such that the file does not appear to have been altered.

#There are three stages to de-obfuscation; they are repeated until an images is found or the search is abandoned:
#1.	Similar to obfuscation-stage-1, the de-obfuscator picks numbers for Y to solve the hash where N=1.
#2.	Set the random number generator with Y
#3.	Attempt to recover a file from the image. If no file is found, return to step 1 but this time with N=N+1.

from scipy import misc
import random
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

#-------Seed related functions-------
def hashPartOfImage(image,bitToUse):
	for i in range(len(image)

def buildSeedFromImage(image,difficulty):
	random.seed(hashPartOfImage(image,2))
	x = hashPartOfImage(image,1)
	for i in range(difficulty):
		x = hashlib.SHA256(x+str(random.random())).hexdigest()
	return int(x,16)
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
	if not checkImageForCompatability(image):
		return
	listOfBits = buildBitList(fileName)
	seed = buildSeedFromImage(image,difficulty)
	stitchBitsToImage(image,seed,listOfBits)
	misc.imsave('new_'+imageName, image)
def decode(imageName):
	image = misc.imread(imageName)
	while(1):
		seed = buildSeedFromImage(image)
		fileName,data = extractDataStream(image,seed)
		if fileName != None:
			break
	buildFile(fileName,data)
if __name__ == '__main__':
	import sys
	if(sys.argv[2] == 'd'):
		decode(sys.argv[1])
	else:
		code(sys.argv[1],sys.argv[2])

