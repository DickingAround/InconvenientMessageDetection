#!/usr/bin/env python
from Crypto.Cipher import AES
import random
import IMDEncryption as encryption
import IMDImageModifier as imageMod
import os
import IMDBitTools as bitTools
import IMDSeedGeneration as seedGeneration
import time
def buildFile(name,data):
	nameParts = name.rsplit('.',1)
	newName = nameParts[0] + '_new.' + nameParts[1]
	f = open(newName,'wb')
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
def code(fileName,imageName,difficultyMultiplier,computeTime):
	image = imageMod.getImageArray(imageName)
	if not imageMod.checkImageForCompatability(imageName):
		print "Imcompatible image; must be tiff, gif, bmp, or png"
		return
	key,iv = seedGeneration.buildKeySetFromImage(image)
	#Compute the hash based on how long we have to do it
	tFinish = time.clock()
	tReport = time.clock()
	i = 1
	while True: #We must do it at least once to reformat the key
		key,iv = seedGeneration.runHashes(key,iv,difficultyMultiplier)
		#keyInt,ivInt = seedGeneration.convertToIntigers(key,iv)
		#print keyInt,ivInt
		if(time.clock() - tReport > 5.0):
			tReport = time.clock()
			print "Working on difficulty %i. Worked %i seconds so far."%((i*difficultyMultiplier),(int(time.clock() - tFinish)))
		if(time.clock() - tFinish > computeTime):
			break
		i += 1
		#if(i == 11):
		#	break
	print "Encoded with difficulty %i"%(i*difficultyMultiplier)
	keyInt,ivInt = seedGeneration.convertToIntigers(key,iv)
	#print keyInt, ivInt
	fileContents = readFile(fileName)
	#print "File length:",len(fileContents)
	encryptedContents = encryption.encrypt(fileContents,keyInt,ivInt)
	#print encryptedContents
	#print "encrypted length:",len(encryptedContents)
	listOfBits = buildBitList(fileName,encryptedContents)
	#print "Bit length:",len(listOfBits)
	imageMod.stitchBitsToImage(image,keyInt,listOfBits)
	imageMod.saveImage(imageName,image)
def decode(imageName,difficultyMultiplier):
	print "Attempting to decode..."
	image = imageMod.getImageArray(imageName)
	key,iv = seedGeneration.buildKeySetFromImage(image)
	#print key,iv
	i = 1
	tReport = time.clock()
	tFinish = time.clock()
	while True:
		if(time.clock() - tReport > 5.0):
			tReport = time.clock()	
			print "Trying with difficulty %i. Worked %i seconds so far."%((difficultyMultiplier*i),(int(time.clock() - tFinish)))
		key,iv = seedGeneration.runHashes(key,iv,difficultyMultiplier)
		keyInt,ivInt = seedGeneration.convertToIntigers(key,iv)
		#print keyInt, ivInt
		pseudoRandomState = random.getstate()
		try:
			fileName,encryptedContents = imageMod.extractDataFromImage(image,keyInt)	
			if fileName != None:
				print "Found it with difficulty %i"%(difficultyMultiplier*i)
				break
		except:
			#print sys.exc_info()	
			#print "Didn't find it"
			1 == 1 #Just keep going
		random.setstate(pseudoRandomState)
		i += 1
		#if(i == 11):
		#	break
	#print encryptedContents
	decryptedContents = encryption.decrypt(encryptedContents,keyInt,ivInt)
	buildFile(fileName,decryptedContents)

if __name__ == '__main__':
	import sys
	difficultyMultiplier = 100000
	if(sys.argv[1] == '-help'):
		print """
./main.py -help
Prints these instructions.

./main.py -t
Runs the unit and integration tests.

./main.py <fileName> <imageName> <numberOfSecondsToUseComputingTheObfuscation>
Obfuscates the file into the image. The new image will have '_new' at the end.

./main.py -d <imageName>
De-obfuscates the file until complete. The new file will have the same name as the origional except with '_new' at the end. If there is no file in the image this will never finish.

"""
	elif(sys.argv[1] == '-t'):
		encryption.IMDEncryption_test()
		imageMod.IMDImageModifier_test()
		bitTools.IMDBitTools_test()
		seedGeneration.IMDSeedGeneration_test()
		os.system('rm testFile_new.txt')
		os.system('rm testImg_new.png')
		code('testFile.txt','testImg.png',difficultyMultiplier,2.0)		
		decode('testImg_new.png',difficultyMultiplier)
		f1 = open('testFile.txt','r')
		f2 = open('testFile_new.txt','r')
		c1 = f1.read()
		c2 = f2.read()
		if(c1 == c2):
			print "Passed: Overall test to encrypt and decrypt"	
		else:
			print "Failed: Overall test to encrypt and decrypt did not match"
	elif(sys.argv[1] == '-d'):
		decode(sys.argv[2],difficultyMultiplier)
	else:
		code(sys.argv[1],sys.argv[2],difficultyMultiplier,int(sys.argv[3]))


