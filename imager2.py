from Crypto.Cipher import AES
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
def readFile(fileName):
	f = open(fileName,'rb')
	data = f.read()
	f.close()
	return data	
def buildBitList(listOfBytes):
	listOfBits = []
	#fileLength*fileName*bitsOfTheFile
	for byte in listOfBytes:
		listOfBits += imageMod.byteToBits(byte)	
	listOfBits = codeString(fileName+"*") + listOfBits
	listOfBits = codeString(str(len(listOfBytes))+"*") + listOfBits
	return listOfBits

#-------Main---------
def code(fileName,imageName):
	image = imageMod.getImageArray(imageName)
	if not imageMod.checkImageForCompatability(imageName):
		print "Imcompatible image; must be tiff, gif, bmp, or png"
		return 
	difficulty = 3
	key,iv = imageMod.buildIntigerSeedFromImage(image,difficulty)
	fileContents = readFile(fileName)
	encryptedContents = encryption.encrypt(fileContents,key,iv)
	listOfBits = buildBitList(encryptedContents)
	imageMod.stitchBitsToImage(image,key,listOfBits)
	misc.imsave('new_'+imageName, image)
def decode(imageName):
	image = misc.imread(imageName)
	difficulty = 1
	while(1):
		seed = imageMod.buildIntigerSeedFromImage(image,difficulty)
		fileName,data = extractDataStream(image,seed)
		if fileName != None:
			break
		difficulty += 1
	buildFile(fileName,data)
if __name__ == '__main__':
	import sys
	if(sys.argv[1] == '-t'):
		code('testFile.txt','testImg.png')		
		#print "No tests"
	elif(sys.argv[2] == 'd'):
		decode(sys.argv[1])
	else:
		code(sys.argv[1],sys.argv[2])


