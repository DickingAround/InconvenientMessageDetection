--------------------How to use it------------------
./main.py -help
Prints these instructions.

./main.py -t
Runs the unit and integration tests.

./main.py <fileName> <imageName> <numberOfSecondsToUseComputingTheObfuscation>
Obfuscates the file into the image. The new image will have '_new' at the end.

./main.py -d <imageName> 
De-obfuscates the file until complete. The new file will have the same name as the origional except with '_new' at the end. If there is no file in the image this will never finish.

--------------------How it works------------------
The problem: Who uses encryption and how much they use it are obvious to mass-observers. Large encryption keys and encrypted data are hard to hide. This leaves the meta-data of communication open for observation. It also leaves people using encryption vulnerable to coercion.

The mission: We want to boil down the meta-data of a message to a single datum; “Is there a secret or not.” If it is reasonable to transmit this datum through insinuation, per-determination, or other methods, then even the existence of a message is hidden.

The strategy: Stenography that requires an uncertain amount of computing effort. In other words, a file is hidden in the unimportant bits of an image such that it requires a user-specified amount of computational effort to extract it. 

When a mass-observer wants to see the meta-data of what communication is going on, they must use compute power to check each image. Because the effort needed to find an image is uncertain to the mass-observer, they never knows for certain if they've worked hard enough. By contrast, the intended recipient of a message presumably got the single datum that a message exists in some public image and will put in as much effort as is needed to find it in a single image. Having every image on the internet be a potential carrier of secrets makes the mass observation of communication meta-data expensive and uncertain.

Even individuals under direct observation can increase their protection with this. An individual may own thousands of images of which only one contains an secret. Until the secret is found by an observer searching every message at possibly great cost, the individual has plausible deny-ability to the secret's existence. This increases their resistance to coercion.

What follows is only a prototype. I am a competent engineers, but not professional in security, encryption, or stenography. I am more than open to advice and help. (And here's thanks to all those who helped craft and refine this idea and implementation so far.)


How does it work, at a high level:

Obfuscation:

1. The image is hashed to create a number. That number is used to encrypt the file to be obfuscated. This encryption is only done to assure the bits of the file are evenly distributes between 0 and 1, it provides no other protection.

2. The image is hashed to create another number. That number is hashed a certain number of times as specified by the user. The result is used to seed a pseudo-random number generator.

3. The speudo-random number generator is then used to decide where to put the 1s and 0s of the file into the image.

4. For each bit, there is a check to see if the pixel being changed will give away that the file exists (e.g. a '1' in a field of '0' saturated color). This check also makes sure we haven't changed the results of previous checks or written to this pixel twice.


De-obfuscation:

1. Same as encryption step 1.

2. Similar to step 2 except that after each hash, the image is checked to see if there is a file in it. This is continued until it finds a file or a the user stops it.

3. Same as encryption step 2.


FAQ:
Q: What about image meta-data? Often images have meta-data about the camera that took them. Is this disturbed? Does it give away the existence of a message?
A: No idea. This is the #1 feature on the list for a V2 of this program.

Q: How are you making it difficult to detect changes in the image?
A: Pixels which are already or near saturated are not used. Also, pixels that are near others with the same value are not used.

Q: Why are you using 'random'? It's well known that this should not be used for encryption.
A: Most encryption wants/needs a random number generator, not a pseudo-random number generator. For example, os.urandom is a source of supposedly actually random numbers. We need a pseudo-random number generator; a random number generator that can be seeded and will repeat itself.

In practice the 'random' library in python is an MT19937 with a period (how often it repeats) of 2^19937 which is to say it is highly impractical/impossible to parallel-test every one of those 2^19937 possible starting positions. Thus the library works fine for this use.

That said, feel free to swap it out for another for your own use.

Q: Why use AES to encrypt the message? 
A: I picked a symmetric encryption algorithm at random. It's only real job is to even the distribution of bits in the secret file such that there's no pattern of more '1's or '0's in the image.

Feel free to swap it out for another for your own use.
