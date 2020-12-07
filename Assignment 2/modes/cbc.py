import numpy as np
from modes.base_mode import BaseMode


class CBCMode(BaseMode):

    def __init__(self, cipher, n=16):
        super(CBCMode, self).__init__(cipher, n=n)

        self._iv = np.random.randint(256, size=(self._n,), dtype=np.uint8).tolist()

    @staticmethod
    def xor_arrays(a, b):
        for i, b_i in enumerate(b):
            a[i] = a[i] ^ b_i

        return a

    def encrypt(self, plaintext: np.array):
        ciphertext = []
        assert len(plaintext) % self._n == 0

        plaintext_list = [plaintext[i * self._n: (i + 1) * self._n].tolist() for i in range(len(plaintext) // self._n)]

        last = self._iv
        for input_subtext in plaintext_list:
            input_subtext = self.xor_arrays(input_subtext, last)
            last = self._cipher.encrypt(input_subtext)
            ciphertext.append(last)

        return np.concatenate(ciphertext).astype(np.uint8)

    def decrypt(self, ciphertext):
        plaintext = []
        assert len(ciphertext) % self._n == 0
        ciphertext_list = [ciphertext[i * self._n: (i + 1) * self._n].tolist() for i in range(len(ciphertext) // self._n)]

        next = self._iv
        for input_subtext in ciphertext_list:
            plainsubtext = self._cipher.decrypt(input_subtext)
            plainsubtext = self.xor_arrays(plainsubtext, next)
            plaintext.append(plainsubtext)
            next = input_subtext

        return np.concatenate(plaintext).astype(np.uint8)


if __name__ == '__main__':
    from ciphers.aes.cipher import AES, AES_TYPE

    key = bytearray.fromhex("000102030405060708090a0b0c0d0e0f")
    key = [w_i for w_i in key]

    aes_cbc_128 = CBCMode(AES(key, AES_TYPE.AES_128), 16)
    PLAINTEXT = np.random.randint(256, size=(16 * 20,), dtype=np.uint8)

    ciphertext = aes_cbc_128.encrypt(PLAINTEXT)
    re_plaintext = aes_cbc_128.decrypt(ciphertext)

    print(np.all(PLAINTEXT == re_plaintext))
