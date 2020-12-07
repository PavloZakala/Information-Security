# AES-and-Kalyna

AES - A class that implements the [AES cipher](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.197.pdf). It has the following methods:

1. `__init__` - the initialization method. Has two parameters: 
    * `key` - Secret, cryptographic key that is used by the Key Expansion routine to generate a set of Round Keys.
    * `aes_type` - { `AES_TYPE.AES_128`, `AES_TYPE.AES_192`, `AES_TYPE.AES_256` }.
2. `encrypt` - the method to encrypt a plaintext to ciphertext. Has the following parameter:
    * `plaintext` - Data input to the Cipher or output from the Inverse Cipher.
3. `decrypt` - the method to decrypt a ciphertext to plaintext. Has the following parameter:
    * `ciphertext` - Data output from the Cipher or input to the Inverse Cipher.
    
    
Kalyna - A class that implements the [Kalyna cipher](https://eprint.iacr.org/2015/650.pdf) . It has the following methods:
1. `__init__` - the initialization method. Has two parameters: 
    * `key` - Secret, cryptographic key that is used by the Key Expansion routine to generate a set of Round Keys.
    * `kalyna_type` - { `KALYNA_TYPE.KALYNA_128_128`, `KALYNA_TYPE.KALYNA_128_256`, `KALYNA_TYPE.KALYNA_256_256`, `KALYNA_TYPE.KALYNA_256_512`, `KALYNA_TYPE.KALYNA_512_512`}.
2. `encrypt` - the method to encrypt a plaintext to ciphertext. Has the following parameter:
    * `plaintext` - Data input to the Cipher or output from the Inverse Cipher.
3. `decrypt` - the method to decrypt a ciphertext to plaintext. Has the following parameter:
    * `ciphertext` - Data output from the Cipher or input to the Inverse Cipher.