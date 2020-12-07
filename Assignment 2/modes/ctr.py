import numpy as np

from modes.base_mode import BaseMode


class CTRMode(BaseMode):
    def __init__(self, cipher, n=16):
        super(CTRMode, self).__init__(cipher, n=n)

        self._iv = bytes(np.random.randint(256, size=(self._n,), dtype=np.uint8).tolist())

    @staticmethod
    def xor_arrays(a, b):
        res = []
        for i, b_i in enumerate(b):
            res.append(a[i] ^ b_i)

        return res

    def encrypt(self, plaintext: np.array):
        ciphertext = []
        assert len(plaintext) % self._n == 0

        plaintext_list = [plaintext[i * self._n: (i + 1) * self._n].tolist() for i in range(len(plaintext) // self._n)]

        for i, plainsubtext in enumerate(plaintext_list):
            nonce = int(int.from_bytes(self._iv, byteorder='big') + i).to_bytes(16, 'big', signed=False)
            ciphersubtext = self.xor_arrays(plainsubtext, self._cipher.encrypt([c for c in nonce]))
            ciphertext.append(ciphersubtext)

        return np.concatenate(ciphertext).astype(np.uint8)

    def decrypt(self, ciphertext):
        plaintext = []
        assert len(ciphertext) % self._n == 0
        ciphertext_list = [ciphertext[i * self._n: (i + 1) * self._n].tolist() for i in
                           range(len(ciphertext) // self._n)]

        for i, ciphersubtext in enumerate(ciphertext_list):
            nonce = int(int.from_bytes(self._iv, byteorder='big') + i).to_bytes(16, 'big', signed=False)
            re_plainsubtext = self.xor_arrays(ciphersubtext, self._cipher.encrypt([c for c in nonce]))
            plaintext.append(re_plainsubtext)

        return np.concatenate(plaintext).astype(np.uint8)


if __name__ == '__main__':
    import os

    np.random.seed(0)
    from ciphers.aes.cipher import AES, AES_TYPE

    key = bytearray.fromhex("000102030405060708090a0b0c0d0e0f")
    key = [w_i for w_i in key]

    aes_ctr_128 = CTRMode(AES(key, AES_TYPE.AES_128), 16)
    PLAINTEXT = np.random.randint(256, size=(16 * 20,), dtype=np.uint8)

    ciphertext = aes_ctr_128.encrypt(PLAINTEXT)
    re_plaintext = aes_ctr_128.decrypt(ciphertext)

    print(np.all(PLAINTEXT == re_plaintext))
