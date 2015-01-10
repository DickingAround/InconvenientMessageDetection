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
def combineBitAndByte(bit,byte):
	return (byte&254)|(bit&1)
def extractBitFromByte(byte):
	return byte&1
def byteArrayToBitArray(s):
	listOfBits = []
	for c in s:
		listOfBits = listOfBits + byteToBits(c)
	return listOfBits
#----------Image tools------------
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

#-------Seed related functions-------
def hashPartOfImage(image,bitToUse):
	#Just read the first line for now
	#TODO: Get a better selection
	s = []
	for i in range(len(image)):
		s += image[i][0][bitToUse]
	return s	

def buildIntigerSeedFromImage(image,difficulty):
	random.seed(hashPartOfImage(image,2))
	x = hashPartOfImage(image,1)
	for i in range(difficulty):
		x = hashlib.SHA256(x+str(random.random())).hexdigest()
	return int(x,16)

#---------Tests---------

def IMDImageModifier_test():
	indexAndLocation_test()
	print "IMDImageModifier tests passed"
  
IMDImageModifier_test()
