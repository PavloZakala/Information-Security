from aes import S_BOX, INV_S_BOX
from aes.key_expansion import key_expansion
from tools import array2state, state2array, xtime, to_bytes


class AES_TYPE:
    AES_128 = {
        "Nk": 4,
        "Nb": 4,
        "Nr": 10
    }

    AES_192 = {
        "Nk": 6,
        "Nb": 4,
        "Nr": 12
    }
    AES_256 = {
        "Nk": 8,
        "Nb": 4,
        "Nr": 14
    }


class AES:

    def __init__(self, key, cipher_type=AES_TYPE.AES_128):
        self._key = key

        self._nk = cipher_type["Nk"]
        self._nb = cipher_type["Nb"]
        self._nr = cipher_type["Nr"]

        self._words = key_expansion(key, self._nb, self._nk, self._nr)

    @staticmethod
    def _sub_bytes(state):

        num_column = len(state)

        for i in range(num_column):
            for j in range(4):
                state[i][j] = S_BOX[state[i][j]]

    @staticmethod
    def _inv_sub_bytes(state):

        num_column = len(state)

        for i in range(num_column):
            for j in range(4):
                state[i][j] = INV_S_BOX[state[i][j]]

    @staticmethod
    def _shift_rows(state):
        state[0][1], state[1][1], state[2][1], state[3][1] = state[1][1], state[2][1], state[3][1], state[0][1]
        state[0][2], state[1][2], state[2][2], state[3][2] = state[2][2], state[3][2], state[0][2], state[1][2]
        state[0][3], state[1][3], state[2][3], state[3][3] = state[3][3], state[0][3], state[1][3], state[2][3]

    @staticmethod
    def _inv_shift_rows(state):
        state[0][1], state[1][1], state[2][1], state[3][1] = state[3][1], state[0][1], state[1][1], state[2][1]
        state[0][2], state[1][2], state[2][2], state[3][2] = state[2][2], state[3][2], state[0][2], state[1][2]
        state[0][3], state[1][3], state[2][3], state[3][3] = state[1][3], state[2][3], state[3][3], state[0][3]

    @staticmethod
    def _mix_columns(state):
        for word in state:
            t = word[0] ^ word[1] ^ word[2] ^ word[3]
            u = word[0]
            word[0] ^= t ^ xtime(word[0] ^ word[1])
            word[1] ^= t ^ xtime(word[1] ^ word[2])
            word[2] ^= t ^ xtime(word[2] ^ word[3])
            word[3] ^= t ^ xtime(word[3] ^ u)

    @staticmethod
    def _inv_mix_columns(state):
        for word in state:
            u = xtime(xtime(word[0] ^ word[2]))
            v = xtime(xtime(word[1] ^ word[3]))
            word[0] ^= u
            word[1] ^= v
            word[2] ^= u
            word[3] ^= v

        AES._mix_columns(state)

    @staticmethod
    def _add_round_key(state, key):
        for word, key_word in zip(state, key):
            for j in range(4):
                word[j] ^= key_word[j]

    def encrypt(self, plaintext):

        state = array2state(plaintext, self._nb)

        self._add_round_key(state, self._words[:self._nb])
        for round in range(1, self._nr):
            self._sub_bytes(state)
            self._shift_rows(state)
            self._mix_columns(state)
            self._add_round_key(state, self._words[round * self._nb: (round + 1) * self._nb])

        self._sub_bytes(state)
        self._shift_rows(state)
        self._add_round_key(state, self._words[self._nr * self._nb: (self._nr + 1) * self._nb])

        return state2array(state)

    def decrypt(self, ciphertext):

        state = array2state(ciphertext, self._nb)

        self._add_round_key(state, self._words[self._nr * self._nb: (self._nr + 1) * self._nb])

        for round in range(self._nr - 1, 0, -1):
            self._inv_shift_rows(state)
            self._inv_sub_bytes(state)
            self._add_round_key(state, self._words[round * self._nb: (round + 1) * self._nb])
            self._inv_mix_columns(state)

        self._inv_shift_rows(state)
        self._inv_sub_bytes(state)
        self._add_round_key(state, self._words[:self._nb])

        return state2array(state)


if __name__ == '__main__':
    key = bytearray.fromhex("000102030405060708090a0b0c0d0e0f")
    key = [w_i for w_i in key]

    aes_128 = AES(key, AES_TYPE.AES_128)

    plain_text = bytearray.fromhex("00112233445566778899aabbccddeeff")
    plain_text = [w_i for w_i in plain_text]

    print(" input:", to_bytes(plain_text, ""))

    output = aes_128.encrypt(plain_text)

    print("output:", to_bytes(output, ""))
    re_input = aes_128.decrypt(output)

    print("rinput:", to_bytes(re_input, ""))

    output = aes_128.encrypt(plain_text)

    print("output:", to_bytes(output, ""))
    re_input = aes_128.decrypt(output)

    print("rinput:", to_bytes(re_input, ""))
