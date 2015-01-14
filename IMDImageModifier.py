import random
import hashlib
from scipy import misc
#-------Bit tools---------
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
def writeBitToByte(bit,byte,bitToUse):
	return (byte&(255-pow(2,bitToUse)))|(bit&pow(2,bitToUse))
def readBitFromByte(byte,bitToUse):
	return (byte&pow(2,bitToUse))>>bitToUse
def byteArrayToBitArray(s):
	listOfBits = []
	for c in s:
		listOfBits = listOfBits + byteToBits(c)
	return listOfBits

def bitFunctions_test():
	if(readBitFromByte(6,0) != 0):
		raise Exception("Failed bit functions test 1")
	if(readBitFromByte(4,2) != 1):
		raise Exception("Failed bit functions test 2")
	return 1

#-------Get image----------
def getImageArray(imageName):
	return misc.imread(imageName)
#-------Image index functions------------
def getIndexOfLocation(image,i,k,j):
	if(i >= len(image) or k >= len(image[0]) or j >= len(image[0][0])):
		raise Exception("Location does not have an index in this image")
	return i*len(image[0])*len(image[0][0]) + k*len(image[0][0]) + j	
def getLocationOfIndex(image,index):
	if(index >= len(image)*len(image[0])*len(image[0][0])):
		raise Exception("Image index out of range for this image")
	i = int(index/(len(image[0][0])*len(image[0])))
	j = int(index/len(image[0][0]))%len(image[0])
	k = index%len(image[0][0])
	return i,j,k
def indexAndLocation_test():
	image = [[[0,0,0] for x in range(7)] for x in range(5)]
	if(getIndexOfLocation(image,1,1,1) != 1*7*3+1*3+1):
		raise Exception("Index and location test 1 failed")
	elif(getIndexOfLocation(image,2,2,2) != 2*7*3+2*3+2):
		raise Exception("Index and location test 2 failed")
	return 1
#-------Image changing functions-------
def extractByteFromImage(image,index):
	bits = []
	for n in range(0,8):
		i,j,k = imageBitIndex(image,index*8+n)
		bits.append(extractBitFromByte(image[i][j][k]))
	return bitsToByte(bits)
def stitchBitsToImage(image,key,bitData):
	random.seed(key)
	#TODO: This needs to actually jump around randomly
	for n in range(0,len(bitData)):
		i,j,k = imageBitIndex(image,n)
		image[i][j][k] = combineBitAndByte(bitData[n],image[i][j][k])

#-------Seed related functions-------
def hashImage(image,bitToUse):
	#Need a string at least 32 long. Take the first 32 rows.
	#For each row, take the bits and group into 8 to turn into chars.
	#TODO: Come up with a better system, 
	c = ''
	bits = [0,0,0,0, 0,0,0,0]
	for i in range(int(len(image)/2),int(len(image)/2)+32):
		for j in range(8):
			bits[j] = readBitFromByte(image[i][int(len(image[0])/2)+j][1],bitToUse) 
		c += bitsToByte(bits)
	return c	
				
def buildIntigerSeedFromImage(image,difficulty):
	randSeed = hashImage(image,2)
	random.seed(randSeed)
	iv = hashlib.sha256(hashImage(image,3)).hexdigest()
	key = hashImage(image,1)
	for i in range(difficulty):
		key = hashlib.sha256(key+str(random.random())).hexdigest()
	return int(key,16), int(iv,16)

def seedAndHash_test():
	image = [[[4,4,4] for x in range(100)] for x in range(100)]
	h_got = hashImage(image,2)
	h_expected = '\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
	if(h_got != h_expected):
		raise Exception("Hash of image test failed")
	buildIntigerSeedFromImage(image,3)
	image = getImageArray("testImg.png")
	buildIntigerSeedFromImage(image,3)
	return 1

#---------Basic tests to make sure this image will work-------
def checkImageForCompatability(imageName):
	imageExtension = imageName.split('.')[1] 
	if imageExtension != 'png' or imageExtension != 'bmp' or imageExtension != 'tiff' or imageExtension != 'gif':
		return 1
	else:
		return 0
		

#---------Tests---------
def IMDImageModifier_test():
	indexAndLocation_test()
	bitFunctions_test()
	seedAndHash_test()
	print "IMDImageModifier tests passed"
  
IMDImageModifier_test()
