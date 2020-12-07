import random
import math

from utils import get_prime, multiplicative_inverse


def generate_key(p, q):
    n = p * q
    phi = (p - 1) * (q - 1)
    e = random.randrange(1, phi)

    g = math.gcd(e, phi)
    while g != 1:
        e = random.randrange(1, phi)
        g = math.gcd(e, phi)

    d = multiplicative_inverse(e, phi)
    dp = d % (p - 1)
    dq = d % (q - 1)

    q_inv = multiplicative_inverse(q, p)

    return (n, e), (p, q, dp, dq, q_inv)


def encrypt(pk, plaintext):
    n, key = pk
    ciphertext = pow(plaintext, key, n)
    return ciphertext


def decrypt(pk, ciphertext):
    p, q, dp, dq, q_inv = pk

    m1 = pow(ciphertext, dp, p)
    m2 = pow(ciphertext, dq, q)
    h = (q_inv * (m1 - m2)) % p
    m = m2 + h * q
    return m


if __name__ == '__main__':
    import os
    from datetime import datetime

    p = 137651541299363631443182998549417268223835422805158282316365973190847982552954231937267097361901548281752237146769189068856418984308914290563863931826142029944054309405136314744235285156821876794429458569215769001959859406949039943326021158141400447906561851655810900268662941832074444774292494390223258514957
    q = 152707703478531033173188950039861733018315313354964276795645138730041583670441862837804867485538543738630086445177955088037540803578096695101641338134581883658399788124267567042949346699425046061550906320595709980729704427014551482718123289979601528481098199101818324439695119855021741855709988787307857456937

    # p = get_prime(1024)
    # q = get_prime(1024)
    # print(p)
    # print(q)

    public_key, private_key = generate_key(p, q)

    print("RSA-Chinese Remainder Theorem")

    for i in [8, 16, 32, 64, 128]:
        plaintext = int.from_bytes(os.urandom(i), 'big')
        print("")
        print("plaintext:", plaintext)
        t1 = datetime.now()
        ciphertext = encrypt(public_key, plaintext)
        t2 = datetime.now()
        print("ciphertext:", ciphertext)
        t3 = datetime.now()
        decrypt_plaintext = decrypt(private_key, ciphertext)
        t4 = datetime.now()
        print("re_plaintext:", decrypt_plaintext)
        print("")
        print("encrypt", t2 - t1)
        print("decrypt", t4 - t3)
        print("")
        print(plaintext == decrypt_plaintext)
