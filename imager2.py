from Crypto.Cipher import AES
import random
import IMDEncryption as encryption
import IMDImageModifier as imageMod
import os
import IMDBitTools as bitTools
import IMDSeedGeneration as seedGeneration
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
def buildBitList(fileName,listOfBytes):
	listOfBits = []
	#fileLength*fileName*bitsOfTheFile
	for byte in listOfBytes:
		listOfBits += bitTools.byteToBits(byte)	
	listOfBits = bitTools.byteArrayToBitArray(fileName+"*") + listOfBits
	listOfBits = bitTools.byteArrayToBitArray(str(len(listOfBytes))+"*") + listOfBits
	return listOfBits

#-------Main---------
def code(fileName,imageName):
	image = imageMod.getImageArray(imageName)
	if not imageMod.checkImageForCompatability(imageName):
		print "Imcompatible image; must be tiff, gif, bmp, or png"
		return 
	difficulty = 3
	key,iv = seedGeneration.buildIntigerSeedFromImage(image,difficulty)
	fileContents = readFile(fileName)
	encryptedContents = encryption.encrypt(fileContents,key,iv)
	listOfBits = buildBitList(fileName,encryptedContents)
	imageMod.stitchBitsToImage(image,key,listOfBits)
	imageMod.saveImage('new_'+imageName,image)
def decode(imageName):
	image = imageMod.getImageArray(imageName)	
	difficulty = 3
	while(1):
		print "Trying with difficulty ",difficulty
		key,iv = seedGeneration.buildIntigerSeedFromImage(image,difficulty)
		fileName,encryptedContents = imageMod.extractDataStream(image,key)	
		if fileName != None:
			break
		difficulty += 1
	decryptedContents = encryption.decrypt(encryptedContents,key,iv)
	buildFile('new_'+fileName,decryptedContents)
if __name__ == '__main__':
	import sys
	if(sys.argv[1] == '-t'):
		os.system('rm new_testFile')
		code('testFile.txt','testImg.png')		
		decode('new_testImg.png')
		f1 = open('testFile.txt','r')
		f2 = open('new_testFile.txt','r')
		c1 = f1.read()
		c2 = f2.read()
		if(c1 == c2):
			print "Passed: Overall test to encrypt and decrypt"	
	elif(sys.argv[2] == 'd'):
		decode(sys.argv[1])
	else:
		code(sys.argv[1],sys.argv[2])


