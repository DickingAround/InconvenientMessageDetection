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

