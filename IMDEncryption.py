from Crypto.Cipher import AES
def encrypt(raw_text, key, iv):
	#return raw_text
	#We don't technically need the initalization vector *and* key here 
	#since we're deriving both from the content, 
	#but no harm in having them and it's better not to break the
	#abstraction the encryption libraries offer
	iv = iv[:16]#IV must be 16 bytes long
	key = key[:32]#key must be 32 bytes long
        encryptor = AES.new(key, AES.MODE_CBC, IV=iv)
        #We want to contain any encrypt-related hacks to the content
        #So we'll add on a number saying how many chars to remove at the end
        numbExtraCharsNeeded = (16-len(raw_text)%16)  
        plain_text = raw_text + (numbExtraCharsNeeded-1)*' ' + hex(numbExtraCharsNeeded)[-1]
	return encryptor.encrypt(plain_text)

def decrypt(cypher_text,key, iv):
	#return cypher_text
	iv = iv[:16]#IV must be 16 bytes long
	key = key[:32]#key must be 32 bytes long
        decryptor = AES.new(key, AES.MODE_CBC, IV=iv)
        plain_text = decryptor.decrypt(cypher_text)
        #Again, remember to cut off the extra data we had to add when encrypting
        raw_text = plain_text[:len(plain_text)-int(plain_text[-1],16)]
        return raw_text

def IMDEncryption_test():
	msg = 'hello world, how are you doing?'
	key = '09123456789012345678901234567890123456789'
	iv = '091234567890123456789'
	msg_encrypted = encrypt(msg,key,iv)
	msg_found = decrypt(msg_encrypted,key,iv)
	if( msg == msg_found):
		print "Passed: IMDEncryption_test"
		return 1
	else:
		print "Failed: IMDEncryption_test"
		print "Old msg: ",msg
		print "New msg: ",msg_found
		return 0

IMDEncryption_test()
