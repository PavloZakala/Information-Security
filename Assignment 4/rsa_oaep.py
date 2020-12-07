import os
import hashlib
import random
import math

from utils import get_prime, multiplicative_inverse, int2bytes, byte_length, bytes2int


def generate_key(p, q):
    n = p * q
    phi = (p - 1) * (q - 1)
    e = random.randrange(1, phi)

    g = math.gcd(e, phi)
    while g != 1:
        e = random.randrange(1, phi)
        g = math.gcd(e, phi)

    d = multiplicative_inverse(e, phi)

    return (n, e), (n, d)


def sha256(message: bytes) -> bytes:
    hasher = hashlib.sha256()
    hasher.update(message)
    return hasher.digest()


def mask_generation(seed: bytes, mlen: int):
    c = 0
    t = b''
    while len(t) < mlen:
        input_bytes = seed + int2bytes(c, 4)
        t += sha256(input_bytes)
        c += 1
    return t[:mlen]


def xor(a_bytes: bytes, b_bytes: bytes) -> bytes:
    return bytes(a ^ b for a, b in zip(a_bytes, b_bytes))


def encrypt(public_key, plaintext, label=b''):
    N, e = public_key
    k = byte_length(N)
    plaintext_len = len(plaintext)
    s = os.urandom(32)

    db = sha256(label) + b'\x00' * (k - plaintext_len - 2 * 32 - 2) + b'\x01' + plaintext

    masked_db = xor(db, mask_generation(s, k - 32 - 1))
    masked_seed = xor(s, mask_generation(masked_db, 32))

    m = bytes2int(b'\x00' + masked_seed + masked_db)
    c = pow(m, e, N)
    return int2bytes(c)


def decrypt(private_key, ciphertext, label=b''):
    n, key = private_key
    plaintext = pow(bytes2int(ciphertext), key, n)
    plaintext = int2bytes(plaintext)

    k = byte_length(n)

    masked_seed, masked_db = plaintext[-(k - 1): -(k - 32 - 1)], plaintext[-(k - 32 - 1):]

    seed = xor(masked_seed, mask_generation(masked_db, 32))
    db = xor(masked_db, mask_generation(seed, k - 32 - 1))

    assert sha256(label) == db[:32]

    i = 32
    while db[i] == 0:
        i += 1
    return db[i + 1:]


if __name__ == '__main__':
    from datetime import datetime

    p = 59385468833864951695227573377119856722748035257056257503313006432254039603512724959791252221321970102601865732206237372103529125718042802174822263256502396406967115760689604507993786699301844521978036648291628075654381736857216793467603917333013397009288391824954557671332913624942254588711665955762671554167
    q = 63287027670804513375716134424031018726807092117014934851394798445725466100622037442935534858384039625758884734400871852231478737169116993486284511410054852986423342628819935309854432273557384624632616342577417318519774507082961822780520302756328503149108177992047988999041478993228976910960111868729269300359

    # p = get_prime()
    # q = get_prime()

    public_key, private_key = generate_key(p, q)

    plaintext = os.urandom(64)

    print("RSA-OAEP")

    for i in [8, 16, 32, 64, 128]:
        plaintext = os.urandom(i)
        print("")
        print("plaintext:", int.from_bytes(plaintext, 'big'))
        t1 = datetime.now()
        ciphertext = encrypt(public_key, plaintext)
        t2 = datetime.now()
        print("ciphertext:", bytes2int(ciphertext))
        t3 = datetime.now()
        decrypt_plaintext = decrypt(private_key, ciphertext)
        t4 = datetime.now()
        print("re_plaintext:", bytes2int(decrypt_plaintext))
        print("")
        print("encrypt", t2 - t1)
        print("decrypt", t4 - t3)
        print("")
        print(plaintext == decrypt_plaintext)