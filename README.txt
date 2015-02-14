Goal: To obscure data in an image such that it takes compute power to find that data.

How does it work, at a high level:
Encyption:
1. The image is hashed to create a number. That number is used to encrypt the file to be obfuscated. This encryption assures the bits of the file are evenly distributes between 0 and 1.
2. The image is hashed to create another number. That number is hashed a certain number of times ('x') as specified by the user. The result is used to seed a pseudo-random number generator. 
3. The speudo-random number generator is then used to decide where the 1s and 0s of the file to be obfuscated into the image. 
4. For each bit, there is a check to see if the pixel being changed will give away that a file is being obfuscated (e.g. a '1' in a field of '0' saturated color).
