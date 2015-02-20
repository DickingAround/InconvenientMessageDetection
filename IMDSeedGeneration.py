import random
import hashlib
import IMDBitTools as bitTools
from scipy import misc
#-------Seed related functions-------
def hashImage(image,bitToUse):
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

def buildKeySetFromImage(image):
	randSeed = hashImage(image,2)
	random.seed(randSeed)
	iv = hashlib.sha256(hashImage(image,3)).hexdigest()
	key = hashImage(image,1)
	return key,iv

def runHashes(key,iv,numberToRun):
	for i in range(numberToRun):
		key = hashlib.sha256(key+str(random.random())).hexdigest()
	return key,iv

def convertToIntigers(key,iv):
	return str(int(key,16)), str(int(iv,16))

'''
def buildIntigerSeedFromImageByDifficulty(image,difficulty):
	keySet = buildKeySetFromImage(image)
	keySet = runHashes(keySet)
	return convertToIntiger(keySet),keySet
	for i in range(difficulty):
		key = hashlib.sha256(key+str(random.random())).hexdigest()
	return str(int(key,16)), str(int(iv,16))
'''
#-------Tests------------------
def IMDSeedGeneration_test():
	image = [[[4,4,4] for x in range(100)] for x in range(100)]
	h_got = hashImage(image,2)
	h_expected = '\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
	if(h_got != h_expected):
		raise Exception("Hash of image test failed")
	key,iv = buildKeySetFromImage(image)
	key,iv = runHashes(key,iv,3)
	keyInt, ivInt = convertToIntigers(key,iv)
	import IMDImageModifier as imdMod
	image = imdMod.getImageArray("testImg.png")
	key,iv = buildKeySetFromImage(image)
	key,iv = runHashes(key,iv,100)
	keyInt, ivInt = convertToIntigers(key,iv)
	print "Passed: IMDSeedGeneration"
	return True

#IMDSeedGeneration_test()
