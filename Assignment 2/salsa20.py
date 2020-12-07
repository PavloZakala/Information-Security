import numpy as np


def to_type(num_array, dtype):
    bytes_array = bytearray(num_array)
    return np.frombuffer(bytes_array, dtype=dtype)


class Salsa:
    MASK = 0xffffffff

    def __init__(self, key, r=20):
        assert r >= 0
        assert len(key) == 32

        self._r = r
        self._key = to_type(np.array(key, dtype=np.uint8), np.uint32).tolist()
        self._nonce = np.random.randint(256, size=(2,), dtype=np.uint32).tolist()

    def _call_salsa(self, message, pos):
        assert len(message) == 4 * 16

        message = to_type(np.array(message, dtype=np.uint8), np.uint32).tolist()

        b = to_type(np.array([pos], dtype=np.uint64), np.uint32).tolist()

        state = [0x61707865, self._key[0], self._key[1], self._key[2],
                 self._key[3], 0x3320646e, self._nonce[0], self._nonce[1],
                 b[0], b[1], 0x79622d32, self._key[4],
                 self._key[5], self._key[6], self._key[7], 0x6b206574]

        for i in range(0, self._r, 2):
            self._quarterround(state, 0, 4, 8, 12)
            self._quarterround(state, 5, 9, 13, 1)
            self._quarterround(state, 10, 14, 2, 6)
            self._quarterround(state, 15, 3, 7, 11)

            self._quarterround(state, 0, 1, 2, 3)
            self._quarterround(state, 5, 6, 7, 4)
            self._quarterround(state, 10, 11, 8, 9)
            self._quarterround(state, 15, 12, 13, 14)

        out = []
        for m, s in zip(message, state):
            out.append(m ^ s)

        return to_type(np.array(out, dtype=np.uint32), np.uint8).tolist()

    @staticmethod
    def _quarterround(state, a, b, c, d):
        state[b] ^= Salsa._rotl32((state[a] + state[d]) & Salsa.MASK, 7)
        state[c] ^= Salsa._rotl32((state[b] + state[a]) & Salsa.MASK, 9)
        state[d] ^= Salsa._rotl32((state[c] + state[b]) & Salsa.MASK, 13)
        state[a] ^= Salsa._rotl32((state[d] + state[c]) & Salsa.MASK, 18)

    @staticmethod
    def _rotl32(w, r):
        return ((w << r) & Salsa.MASK) | (w >> (32 - r))

    def encrypt(self, plaintext):
        assert len(plaintext) % (4 * 16) == 0

        n = len(plaintext) // (4 * 16)

        ciphertext = []
        for i in range(n):
            ciphersubtext = self._call_salsa(plaintext[i * (4 * 16): (i + 1) * (4 * 16)], i)
            ciphertext.append(ciphersubtext)

        return np.concatenate(ciphertext).astype(np.uint8)

    def decrypt(self, ciphertext):
        assert len(ciphertext) % (8 * 16) == 0

        n = len(ciphertext) // (8 * 16)

        plaintext = []
        for i in range(n):
            re_plainsubtext = self._call_salsa(ciphertext[i * (4 * 16): (i + 1) * (4 * 16)], i)
            plaintext.append(re_plainsubtext)

        return np.concatenate(plaintext).astype(np.uint8)


if __name__ == '__main__':
    KEY = np.arange(32, dtype=np.uint8)

    salsa20 = Salsa(KEY)
    PLAINTEXT = np.random.randint(256, size=(16 * 4 * 10,), dtype=np.uint8).tolist()

    ciphertext = salsa20.encrypt(PLAINTEXT)
    re_plaintext = salsa20.encrypt(ciphertext)
    print(all([r == p for r, p in zip(re_plaintext, PLAINTEXT)]))
