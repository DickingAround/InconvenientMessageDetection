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
Goal: To obscure data in an image such that it takes compute power to find that data.

How does it work, at a high level:
Encyption:
1. The image is hashed to create a number. That number is used to encrypt the file to be obfuscated. This encryption assures the bits of the file are evenly distributes between 0 and 1.
2. The image is hashed to create another number. That number is hashed a certain number of times ('x') as specified by the user. The result is used to seed a pseudo-random number generator. 
3. The speudo-random number generator is then used to decide where the 1s and 0s of the file to be obfuscated into the image. 
4. For each bit, there is a check to see if the pixel being changed will give away that a file is being obfuscated (e.g. a '1' in a field of '0' saturated color). If the pixel fails before or after the change, the bit is reverted and a different one is picked. 

Decryption:
1. Same as encryption step 1.
2. Similar to step 2 except that after each hash, the image is checked to see if there is a file in it. This is continued until it finds a file or a the user stops it.
3. Same as encryption step 2.
