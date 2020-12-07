import numpy as np

from string_tools import encode, decode

class RC4:
    class __RC4Tools:

        def _s_init(self, key):
            key_length = len(key)

            self._s = np.arange(256, dtype=np.uint8)
            j = 0
            for i in range(256):
                j = (j + self._s[i] + key[i % key_length]) % 256
                self._s[i], self._s[j] = self._s[j], self._s[i]

        def __init__(self, key):
            self._s_init(key)

        def apply_key(self, data):
            res = []
            i = 0
            j = 0
            for item in data:
                i = (i + 1) % 256
                j = (j + self._s[i]) % 256
                self._s[i], self._s[j] = self._s[i], self._s[j]
                res.append(item ^ self._s[(self._s[i] + self._s[j]) % 256])

            return np.array(res, dtype=np.uint8)

    def __init__(self, key):

        self._encoder = self.__RC4Tools(key)
        self._decoder = self.__RC4Tools(key)

    def encrypt(self, plaintext):
        return self._encoder.apply_key(plaintext)

    def decrypt(self, ciphertext):
        return self._decoder.apply_key(ciphertext)


if __name__ == '__main__':
    key = bytearray.fromhex("000102030405060708090a0b0c0d0e0f")
    KEY = [w_i for w_i in key]
    # KEY = encode("Key")
    rc4 = RC4(KEY)
    PLAINTEXT = encode("Plaintext")

    ciphertext = rc4.encrypt(PLAINTEXT)
    res = rc4.decrypt(ciphertext)
    print(decode(res))
