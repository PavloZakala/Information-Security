import numpy as np
import random
import math

from miller_rabin_test import miller_rabin_test

def byte_length(n):
    return math.ceil(n.bit_length() / 8)


def bytes2int(bytes):
    return int.from_bytes(bytes, 'big')


def int2bytes(n, fill_size=-1):
    bytes_required = fill_size if fill_size != -1 else byte_length(n)
    return n.to_bytes(bytes_required, 'big')

def get_prime(bin_len):
    n = random.randrange(2 ** (bin_len-1)-1, 2 ** bin_len-1, 2)
    while not miller_rabin_test(n):
        n += 1
    return n


def multiplicative_inverse(e, phi):
    d, x1, x2, y1 = 0, 0, 1, 1
    temp_phi = phi

    while e > 0:
        temp1 = temp_phi // e
        temp2 = temp_phi - temp1 * e
        temp_phi = e
        e = temp2

        x2, x1 = x1, x2 - temp1 * x1
        d, y1 = y1, d - temp1 * y1

    if temp_phi == 1:
        return d + phi