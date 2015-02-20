import random
import hashlib
import IMDBitTools as bitTools
from scipy import misc
#-------Get image----------
def getImageArray(imageName):
	return misc.imread(imageName)
def saveImage(name, image):
	nameParts = name.rsplit('.',1)
	newName = nameParts[0] + '_new.' + nameParts[1]
	misc.imsave(newName, image)

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
	global usedPixels	
	usedPixels = {}
	global imageIndexMax 
	imageIndexMax = len(image)*len(image[0])*len(image[0][0])
def randomlyFindNextPixel(image):
	global imageIndexMax
	return getLocationOfIndex(image,int(random.random()*imageIndexMax))
#-------Functions to check if this bit is safe to change--------
def checkThisPixel(i,j,k):
	s = str(i)+'-'+str(j)+'-'+str(k)
	if not s in usedPixels:
		return True
def checkAndMarkThisPixel(i,j,k):
	#We actually want to check every pixel around this one as well
	#If others nearby are being used, then changing this one could affect the valididty of those pixels and we're not checking their validity
	#Of course we could check their validity but that's actually a bit more complex and I suspect more expensive.
	if(	checkThisPixel(i+1,j  ,k) and
		checkThisPixel(i+1,j+1,k) and 
		checkThisPixel(i+1,j-1,k) and 
		checkThisPixel(i  ,j  ,k) and 
		checkThisPixel(i  ,j+1,k) and 
		checkThisPixel(i  ,j-1,k) and 
		checkThisPixel(i-1,j  ,k) and 
		checkThisPixel(i-1,j+1,k) and 
		checkThisPixel(i-1,j-1,k)):
		s = str(i)+'-'+str(j)+'-'+str(k)
		usedPixels[s] = True
		return True
	if (len(usedPixels) > 0.1*imageIndexMax): 
		#10% is just an approximation of when the image is getting full. 
		#The real number will depend on the image. 
		#We just want to pick a number that eventually terminates,
		#which is any number substantially less than 25% based on how pixels are checked off.
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
	if(nearbyColors.count(thisColor) > 2): #TODO: Is 2 the right number? We want something that doesn't give away our pixel. 
		#print "rejected on too similar"
		return True
	return False
	
def isThisPixelSaturated(image,i,j,k):
	if(getColorSafely(image,i,j,j) in [0,1,254,255]):
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
	return True

#-------Image changing functions-------
def stitchBitsToImage(image,key,bitData):
	resetCountersForPixelChanging(image,key)
	n = 0
	index = 0
	f = open('PixelLogIn.txt','w')
	while n < len(bitData):
		i,j,k = randomlyFindNextPixel(image)
		#i,j,k = getLocationOfIndex(image,index)
		if(checkAndMarkThisPixel(i,j,k) and isThisPixelSafe(image,i,j,k)):
			oldColor = image[i][j][k]
			image[i][j][k] = bitTools.writeBitToByte(bitData[n],image[i][j][k],0)
			if(isThisPixelSafe(image,i,j,k)): #Did changing it make it unsafe now?
				n += 1
				f.write("%i,%i,%i\n"%(i,j,k))
			#else:
				#if(i == 98 and j == 245 and k == 0):
					#print "Pixel made unsafe"
				#Don't revet it, we need to keep it broken so the decryption side isn't confused and get an off-by-1 error on it
				#image[i][j][k] = oldColor	
		index += 1
	f.close()

def extractByteFromImage(image,index,f):
	bits = []
	n = 0
	while n < 8:
		i,j,k = randomlyFindNextPixel(image)
		#i,j,k = getLocationOfIndex(image,index)
		if(checkAndMarkThisPixel(i,j,k) and isThisPixelSafe(image,i,j,k)):
			bits.append(bitTools.readBitFromByte(image[i][j][k],0))
			n += 1
			f.write("%i,%i,%i\n"%(i,j,k))
		#else:
			#print "Not reading from %i,%i,%i"%(i,j,k)
		index += 1	
	return index,bitTools.bitsToByte(bits)
def extractDataFromImage(image,key):
	resetCountersForPixelChanging(image,key)
	data = []
	fileName = ''
	byteLenghtValue = 0
	#-- Get the length --
	byteLengthString = ''
	currentByte = '-'
	i = 0
	f = open('PixelLogOut.txt','w')
	while(currentByte != '*'):
		i,currentByte = extractByteFromImage(image,i,f)
		byteLengthString += currentByte
		if(len(byteLengthString) > 10):
			#There should not be more than 10G files hiding in theimage..
			#Clearly we're getting garbage data
			raise Exception("File length is an incorrectly long string")
	byteLengthValue = int(byteLengthString[:len(byteLengthString)-1])
	#-- Get the name --
	currentByte = '-'
	while(currentByte != '*'):
		i,currentByte = extractByteFromImage(image,i,f)
                fileName += currentByte
	fileName = fileName[:len(fileName)-1]
	#-- Get the data --
	for j in range(byteLengthValue):
		i,currentByte = extractByteFromImage(image,i,f)
		data.append(currentByte)
	contents = ''.join(data)
	f.close()
	return fileName,contents

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
  
#IMDImageModifier_test()
