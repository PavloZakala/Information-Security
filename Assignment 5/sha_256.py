K = [
    0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
    0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
    0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
    0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
    0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
    0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
    0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
    0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
]

MOD = 2 ** 32


def _rotate_right(num: int, shift: int, size: int = 32):
    return (num >> shift) | (num << size - shift)


def _sigma0(num: int):
    num = (_rotate_right(num, 7) ^
           _rotate_right(num, 18) ^
           (num >> 3))
    return num


def _sigma1(num: int):
    num = (_rotate_right(num, 17) ^
           _rotate_right(num, 19) ^
           (num >> 10))
    return num


def sha_256(message: bytearray) -> bytearray:
    # Padding
    length = len(message) * 8
    message.append(0x80)
    while (len(message) * 8 + 64) % 512 != 0:
        message.append(0x00)

    message += length.to_bytes(8, 'big')
    blocks = [message[i:i + 64] for i in range(0, len(message), 64)]

    # Setting Initial Hash Value
    h0 = 0x6a09e667
    h1 = 0xbb67ae85
    h2 = 0x3c6ef372
    h3 = 0xa54ff53a
    h5 = 0x9b05688c
    h4 = 0x510e527f
    h6 = 0x1f83d9ab
    h7 = 0x5be0cd19

    for message_block in blocks:
        message_schedule = []
        for t in range(0, 64):
            if t <= 15:
                message_schedule.append(bytes(message_block[t * 4:(t * 4) + 4]))
            else:
                term1 = _sigma1(int.from_bytes(message_schedule[t - 2], 'big'))
                term2 = int.from_bytes(message_schedule[t - 7], 'big')
                term3 = _sigma0(int.from_bytes(message_schedule[t - 15], 'big'))
                term4 = int.from_bytes(message_schedule[t - 16], 'big')

                schedule = ((term1 + term2 + term3 + term4) % MOD).to_bytes(4, 'big')
                message_schedule.append(schedule)

        a = h0
        b = h1
        c = h2
        d = h3
        e = h4
        f = h5
        g = h6
        h = h7

        # Iterate for t=0 to 63
        for t in range(64):
            sigma1 = (_rotate_right(e, 6) ^ _rotate_right(e, 11) ^ _rotate_right(e, 25))
            ch = (e & f) ^ (~e & g)
            t1 = ((h + sigma1 + ch + K[t] + int.from_bytes(message_schedule[t], 'big')) % MOD)
            sigma0 = (_rotate_right(a, 2) ^ _rotate_right(a, 13) ^ _rotate_right(a, 22))
            Ma = (a & b) ^ (a & c) ^ (b & c)
            t2 = (sigma0 + Ma) % MOD

            h = g
            g = f
            f = e
            e = (d + t1) % MOD
            d = c
            c = b
            b = a
            a = (t1 + t2) % MOD

        # Compute intermediate hash value
        h0 = (h0 + a) % MOD
        h1 = (h1 + b) % MOD
        h2 = (h2 + c) % MOD
        h3 = (h3 + d) % MOD
        h4 = (h4 + e) % MOD
        h5 = (h5 + f) % MOD
        h6 = (h6 + g) % MOD
        h7 = (h7 + h) % MOD

    return ((h0).to_bytes(4, 'big') + (h1).to_bytes(4, 'big') +
            (h2).to_bytes(4, 'big') + (h3).to_bytes(4, 'big') +
            (h4).to_bytes(4, 'big') + (h5).to_bytes(4, 'big') +
            (h6).to_bytes(4, 'big') + (h7).to_bytes(4, 'big'))

