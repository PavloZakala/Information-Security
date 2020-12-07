from aes import S_BOX, R_CON
from tools import print_state


def rot_word(word):
    word.append(word.pop(0))
    return word


def sub_word(word):
    return [S_BOX[byte] for byte in word]


def key_expansion(key, nb, nk, nr):
    words = []
    for i in range(nk):
        words.append(key[nb * i: nb * (i + 1)])

    for i in range(nk, nb * (nr + 1)):
        temp = words[-1][:]
        if i % nk == 0:
            temp = sub_word(rot_word(temp))
            temp[0] ^= R_CON[(i // nk)]
        elif nk > 6 and i % nk == 4:
            temp = sub_word(temp)

        for j in range(len(temp)):
            temp[j] ^= words[-nk][j]

        words.append(temp)

    return words


if __name__ == '__main__':
    # AES-128 4 4 10
    print("AES-128 4 4 10")
    w0 = bytearray.fromhex("2b7e1516")
    w1 = bytearray.fromhex("28aed2a6")
    w2 = bytearray.fromhex("abf71588")
    w3 = bytearray.fromhex("09cf4f3c")

    key = [w_i for w_i in w0 + w1 + w2 + w3]
    words = key_expansion(key, 4, 4, 10)
    print_state(words)

    # AES-192 4 6 12
    print("\n****************\n")
    print("AES-192 4 6 12")
    w0 = bytearray.fromhex("8e73b0f7")
    w1 = bytearray.fromhex("da0e6452")
    w2 = bytearray.fromhex("c810f32b")
    w3 = bytearray.fromhex("809079e5")
    w4 = bytearray.fromhex("62f8ead2")
    w5 = bytearray.fromhex("522c6b7b")

    key = [w_i for w_i in w0 + w1 + w2 + w3 + w4 + w5]
    words = key_expansion(key, 4, 6, 12)
    print_state(words)

    # AES-256 4 8 14
    print("\n****************\n")
    print("AES-256 4 8 14")
    w0 = bytearray.fromhex("603deb10")
    w1 = bytearray.fromhex("15ca71be")
    w2 = bytearray.fromhex("2b73aef0")
    w3 = bytearray.fromhex("857d7781")
    w4 = bytearray.fromhex("1f352c07")
    w5 = bytearray.fromhex("3b6108d7")
    w6 = bytearray.fromhex("2d9810a3")
    w7 = bytearray.fromhex("0914dff4")

    key = [w_i for w_i in w0 + w1 + w2 + w3 + w4 + w5 + w6 + w7]
    words = key_expansion(key, 4, 8, 14)
    print_state(words)
