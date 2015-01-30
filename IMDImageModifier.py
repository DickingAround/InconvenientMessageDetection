import random
import hashlib
import IMDBitTools as bitTools
from scipy import misc
#-------Bit tools---------
'''def bitsToByte(bits):
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
'''
#-------Get image----------
def getImageArray(imageName):
	return misc.imread(imageName)
def saveImage(name, image):
	misc.imsave(name, image)

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

#-------Pixel placing functions--------
usedPixels = {}
imageIndexMax = 0
def resetCountersForPixelChanging(image,key):
	random.seed(key)
	print "Resetting with key:"
	print key
	global usedPixels	
	usedPixels = {}
	global imageIndexMax 
	imageIndexMax = len(image)*len(image[0])*len(image[0][0])
def randomlyFindNextPixel(image):
	global imageIndexMax
	return getLocationOfIndex(image,int(random.random()*imageIndexMax))
#-------Functions to check if this bit is safe to change--------
def checkAndMarkThisPixel(i,j,k):
	s = str(i)+'-'+str(j)+'-'+str(k)
	if not s in usedPixels:
		usedPixels[s] = True
		return True
	if (len(usedPixels) > 0.1*imageIndexMax):
		raise Exception("The image is too small to contain this data.")
	return False
def getColorSafely(image,i,j,k):
	return image[i%len(image)][j%len(image[0])][k%len(image[0][0])]
def areTheNearbyPixelsTooSimilar(image,i,j,k):
	thisColor = getColorSafely(image,i,j,k)
	nearbyColors = []
	nearbyColors.append(getColorSafely(image,i+1,j,k))
	nearbyColors.append(getColorSafely(image,i+1,j+1,k))
	nearbyColors.append(getColorSafely(image,i+1,j-1,k))
	nearbyColors.append(getColorSafely(image,i-1,j,k))
	nearbyColors.append(getColorSafely(image,i-1,j+1,k))
	nearbyColors.append(getColorSafely(image,i-1,j-1,k))
	nearbyColors.append(getColorSafely(image,i  ,j+1,k))
	nearbyColors.append(getColorSafely(image,i  ,j-1,k))
	if(nearbyColors.count(thisColor) > 9):
		#print "I am rejecting this pixel as similar"
		print nearbyColors
		return True
	return False
	
def isThisPixelSaturated(image,i,j,k):
	if(getColorSafely(image,i,j,j) in [0,1,254,255]):
		#print "I am rejecting this pixel as saturated"
		return True
	return False
def isThisPixelSafe(image,i,j,k):
	#If any color of this bit is saturated
	#Or if a nearby bit is saturated
	#Or if this color is too close to a nearby colora
	#Or if we already changed this bit
	#TODO: Turn this back on	
	if(areTheNearbyPixelsTooSimilar(image,i,j,k)):
		return False
	if isThisPixelSaturated(image,i,j,k):
		return False
	if isThisPixelSaturated(image,i+1,j,k):
		return False
	if isThisPixelSaturated(image,i-1,j,k):
		return False
	if isThisPixelSaturated(image,i,j+1,k):
		return False
	if isThisPixelSaturated(image,i,j-1,k):
		return False
	#if checkAndMarkThisPixel(i,j,k):
	#	return True
	#print "I am accepting this pixel"
	return True
#-------Image changing functions-------
def stitchBitsToImage(image,key,bitData):
	resetCountersForPixelChanging(image,key)
	#TODO: This needs to actually jump around randomly
	n = 0
	index = 0
	while n < len(bitData):
		i,j,k = randomlyFindNextPixel(image)
		#i,j,k = getLocationOfIndex(image,index)
		if(checkAndMarkThisPixel(i,j,k) and isThisPixelSafe(image,i,j,k)):
			#print "Writing to %i,%i,%i,%i"%(index,i,j,k)
			oldColor = image[i][j][k]
			image[i][j][k] = bitTools.writeBitToByte(bitData[n],image[i][j][k],0)
			if(isThisPixelSafe(image,i,j,k)): #Did changing it make it unsafe now?
				#print "Good pixel"
				n += 1
			else:
				#print "No good"
				image[i][j][k] = oldColor	
		#else:
		#	print "pixel was unsafe"
		index += 1
		#if(n%8 == 0):
			#print "Pushing index %i"%index
			

def extractByteFromImage(image,index):
	bits = []
	n = 0
	while n < 8:
		i,j,k = randomlyFindNextPixel(image)
		#i,j,k = getLocationOfIndex(image,index)
		if(checkAndMarkThisPixel(i,j,k) and isThisPixelSafe(image,i,j,k)):
			#print "Reading from %i,%i,%i,%i"%(index,i,j,k)
			bits.append(bitTools.readBitFromByte(image[i][j][k],0))
			n += 1
		#else:
			#print "Not reading from %i,%i,%i"%(i,j,k)
		index += 1	
	#print "Extracting index %i"%index
	return index,bitTools.bitsToByte(bits)
def extractDataStream(image,key):
	resetCountersForPixelChanging(image,key)
	data = []
	fileName = ''
	byteLenghtValue = 0
	#-- Get the length --
	byteLengthString = ''
	currentByte = '-'
	i = 0
	while(currentByte != '*'):
		i,currentByte = extractByteFromImage(image,i)
		#print currentByte
		byteLengthString += currentByte
	byteLengthValue = int(byteLengthString[:len(byteLengthString)-1])
	print "Im about to get %i"%byteLengthValue	
	#-- Get the name --
	currentByte = '-'
	while(currentByte != '*'):
		i,currentByte = extractByteFromImage(image,i)
                fileName += currentByte
		#print currentByte
	fileName = fileName[:len(fileName)-1]
	#-- Get the data --
	for j in range(byteLengthValue):
		i,currentByte = extractByteFromImage(image,i)
		data.append(currentByte)
		#print currentByte
	contents = ''.join(data)
	return fileName,contents

#-------Seed related functions-------
'''def hashImage(image,bitToUse):
	#Need a string at least 32 long. Take the first 32 rows.
	#For each row, take the bits and group into 8 to turn into chars.
	#TODO: Come up with a better system, 
	c = ''
	bits = [0,0,0,0, 0,0,0,0]
	for i in range(int(len(image)/2),int(len(image)/2)+32):
		for j in range(8):
			bits[j] = bitTools.readBitFromByte(image[i][int(len(image[0])/2)+j][1],bitToUse) 
		c += bitTools.bitsToByte(bits)
	return c	
				
def buildIntigerSeedFromImage(image,difficulty):
	randSeed = hashImage(image,2)
	random.seed(randSeed)
	iv = hashlib.sha256(hashImage(image,3)).hexdigest()
	key = hashImage(image,1)
	for i in range(difficulty):
		key = hashlib.sha256(key+str(random.random())).hexdigest()
	return str(int(key,16)), str(int(iv,16))

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
'''
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
	#seedAndHash_test()
	print "Passed: IMDImageModifier tests"
  
IMDImageModifier_test()
