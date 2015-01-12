#There are three stages to obfuscating: 
#1.	Similar to mining on the bitcoin block chain, build a number (‘X’) is generated from the base image. Then you try many random numbers (‘Y’) until the the result of SHA265(X+Y) has a certain number of 1s (‘N’) at the beginning of it. The user picks N. The larger N they pick, the harder their computer must work doing hashes until the file can be obfuscated into the image (the de-obfuscator will also work harder, as we’ll later see). 
#2.	The number Y is used to seed a pseudo-random number generator. The output of this generator decides where in the image to place the bits of the file being obfuscated. 
#3.	The low-impact bits of the image are changed to ‘1’ or ‘0’ while also checking to make sure a pixel in the image is never written twice, a saturated color is not changed, etc. such that the file does not appear to have been altered.

#There are three stages to de-obfuscation; they are repeated until an images is found or the search is abandoned:
#1.	Similar to obfuscation-stage-1, the de-obfuscator picks numbers for Y to solve the hash where N=1.
#2.	Set the random number generator with Y
#3.	Attempt to recover a file from the image. If no file is found, return to step 1 but this time with N=N+1.

from Crypto.Cipher import AES
from scipy import misc
import random
import IMDEncryption as encryption
import IMDImageModifier as imageMod

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
		currentByte = imageMod.extractByteFromImage(image,i)
		byteLengthString += currentByte
		i += 1
	byteLengthValue = int(byteLengthString[:len(byteLengthString)-1])
	#-- Get the name --
	currentByte = '-'
	while(currentByte != '*'):	
		currentByte = imageMod.extractByteFromImage(image,i)
		fileName += currentByte
		i += 1
	fileName = fileName[:len(fileName)-1]
	#-- Get the data --
	for j in range(i,i+byteLengthValue):
		data.append(imageMod.extractByteFromImage(image,j))
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
		listOfBits += imageMod.byteToBits(byte)	
		byte = f.read(1)
	f.close()
	listOfBits = codeString(fileName+"*") + listOfBits
	listOfBits = codeString(str(bytesRead)+"*") + listOfBits
	return listOfBits

#-------Main---------
def code(fileName,imageName):
	image = misc.imread(imageName)
	if not imageMod.checkImageForCompatability(imageName):
		print "Imcompatible image; must be tiff, gif, bmp, or png"
		return 
	seed = imageMod.buildIntigerSeedFromImage(image,difficulty)
	fileContents = readFile(fileName)
	encryptedContents = encryption.encrypt(fileContents,seed)
	listOfBits = imageMod.buildBitList(encryptedContents)
	imageMod.stitchBitsToImage(image,seed,listOfBits)
	misc.imsave('new_'+imageName, image)
def decode(imageName):
	image = misc.imread(imageName)
	difficulty = 0
	while(1):
		seed = imageMod.buildIntigerSeedFromImage(image,difficulty)
		fileName,data = extractDataStream(image,seed)
		if fileName != None:
			break
		difficulty += 1
	buildFile(fileName,data)
if __name__ == '__main__':
	import sys
	if(sys.argv[2] == 'd'):
		decode(sys.argv[1])
	else:
		code(sys.argv[1],sys.argv[2])

