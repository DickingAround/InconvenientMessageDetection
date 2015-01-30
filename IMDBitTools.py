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
def writeBitToByte(bit,byte,bitToUse):
	return (byte&(255-pow(2,bitToUse)))|(bit&pow(2,bitToUse))
def readBitFromByte(byte,bitToUse):
	return (byte&pow(2,bitToUse))>>bitToUse
def byteArrayToBitArray(s):
	listOfBits = []
	for c in s:
		listOfBits = listOfBits + byteToBits(c)
	return listOfBits

#---------Tests---------
def IMDBitTools_test():
	if(readBitFromByte(6,0) != 0):
		raise Exception("Failed bit functions test 1")
	if(readBitFromByte(4,2) != 1):
		raise Exception("Failed bit functions test 2")
	print "Passed: IMDImageModifier tests"
	return True

IMDBitTools_test()
