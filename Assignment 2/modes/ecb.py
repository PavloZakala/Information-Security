import numpy as np
from modes.base_mode import BaseMode


class ECBMode(BaseMode):

    def encrypt(self, plaintext: np.array):
        ciphertext = []
        assert len(plaintext) % self._n == 0

        for i in range(len(plaintext) // self._n):
            ciphersubtext = np.array(self._cipher.encrypt(plaintext[i * self._n: (i + 1) * self._n].tolist()),
                                     dtype=np.uint8)
            ciphertext.append(ciphersubtext)

        return np.concatenate(ciphertext).astype(np.uint8)

    def decrypt(self, ciphertext):
        plaintext = []
        assert len(ciphertext) % self._n == 0

        for i in range(len(ciphertext) // self._n):
            plaintext.append(self._cipher.decrypt(ciphertext[i * self._n: (i + 1) * self._n].tolist()))

        return np.concatenate(plaintext).astype(np.uint8)


if __name__ == '__main__':
    from ciphers.aes.cipher import AES, AES_TYPE

    key = bytearray.fromhex("000102030405060708090a0b0c0d0e0f")
    key = [w_i for w_i in key]

    aes_ecb_128 = ECBMode(AES(key, AES_TYPE.AES_128), 16)
    PLAINTEXT = np.random.randint(256, size=(16 * 20,), dtype=np.uint8)

    ciphertext = aes_ecb_128.encrypt(PLAINTEXT)
    re_plaintext = aes_ecb_128.decrypt(ciphertext)

    print(np.all(PLAINTEXT == re_plaintext))
