#!/usr/bin/env python
from Crypto.Cipher import AES
import random
import IMDEncryption as encryption
import IMDImageModifier as imageMod
import os
import IMDBitTools as bitTools
import IMDSeedGeneration as seedGeneration
import time

#-------File writing functions---------
def writeFile(name,data):
	#Add 'new' to the name of any encoded file so anyone 
	#testing it doesn't accidentialy overwrite their origional file.
	nameParts = name.rsplit('.',1)
	newName = nameParts[0] + '_new.' + nameParts[1]
	print "Writing file '"+ newName + "'"
	f = open(newName,'wb')
	for c in data:
		f.write(c)
	f.close()	
def readFile(fileName):
	f = open(fileName,'rb')
	data = f.read()
	f.close()
	return data	

#-------Core code and decode workflows---------
def code(fileName,imageName,difficultyMultiplier,computeTime):
	#Load the image
	image = imageMod.getImageArray(imageName)
	if not imageMod.checkImageForCompatability(imageName):
		print "Imcompatible image; must be tiff, gif, bmp, or png"
		return

	#Create the keys used to encode the data
	key,iv = seedGeneration.buildKeySetFromImage(image)
	tFinish = time.clock() #Track total CPU time used so far
	tReport = time.clock() #Track time until next update to the user
	i = 1 #Track now many times we hash, just to tell the user
	while True: #We must hash at least once to reformat the key
		key,iv = seedGeneration.runHashes(key,iv,difficultyMultiplier)
		if(time.clock() - tReport > 5.0):
			tReport = time.clock()
			print "Working on difficulty %i. Worked %i seconds so far."%((i*difficultyMultiplier),(int(time.clock() - tFinish)))
		if(time.clock() - tFinish > computeTime):
			break
		i += 1
	print "Encoding with difficulty %i"%(i*difficultyMultiplier)
	keyInt,ivInt = seedGeneration.convertToIntigers(key,iv)

	#Read the file, encrypt it, and build the special bitstream needed
	fileContents = readFile(fileName)
	encryptedContents = encryption.encrypt(fileContents,keyInt,ivInt)
	listOfBits = imageMod.buildBitList(fileName,encryptedContents)

	#Modify the image and save it under a new name
	imageMod.stitchBitsToImage(image,keyInt,listOfBits)
	imageMod.saveImage(imageName,image)

def decode(imageName,difficultyMultiplier):
	print "Attempting to decode..."
	#Load the image
	image = imageMod.getImageArray(imageName)

	#Search for a key to the image
	key,iv = seedGeneration.buildKeySetFromImage(image)
	i = 1
	tReport = time.clock()
	tFinish = time.clock()
	while True:
		if(time.clock() - tReport > 5.0):
			tReport = time.clock()	
			print "Trying with difficulty %i. Worked %i seconds so far."%((difficultyMultiplier*i),(int(time.clock() - tFinish)))
		key,iv = seedGeneration.runHashes(key,iv,difficultyMultiplier)
		keyInt,ivInt = seedGeneration.convertToIntigers(key,iv)
		pseudoRandomState = random.getstate()
		try:
			fileName,encryptedContents = imageMod.extractDataFromImage(image,keyInt)	
			if fileName != None:
				print "Found it with difficulty %i"%(difficultyMultiplier*i)
				break
		except:
			1 == 1 #Just keep going, try a new one
		random.setstate(pseudoRandomState)
		i += 1

	#Now that we have the extracted data, decrypt and save it
	decryptedContents = encryption.decrypt(encryptedContents,keyInt,ivInt)
	writeFile(fileName,decryptedContents)

if __name__ == '__main__':
	import sys
	difficultyMultiplier = 100000
	#--- HELP ---
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
	#--- TEST ---
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
	#--- DECODE ---
	elif(sys.argv[1] == '-d'):
		decode(sys.argv[2],difficultyMultiplier)
	#--- ENCODE ---
	else:
		code(sys.argv[1],sys.argv[2],difficultyMultiplier,int(sys.argv[3]))


