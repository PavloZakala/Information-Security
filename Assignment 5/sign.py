import random

from elliptic_curve import Curve
from sha_256 import sha_256


class ECDSA:
    CURVE = Curve(A=1,
                  B=0x03CE10490F6A708FC26DFE8C3D27C4F94E690134D5BFF988D8D28AAEAEDE975936C66BAC536B18AE2DC312CA493117DAA469C640CAF3,
                  n=0x3FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFBA3175458009A8C0A724F02F81AA8A1FCBAF80D90C7A95110504CF
                  )
    BASE_X = 0x1A62BA79D98133A16BBAE7ED9A8E03C32E0824D57AEF72F88986874E5AAE49C27BED49A2A95058068426C2171E99FD3B43C5947C857D
    BASE_Y = 0x70B5E1E14031C1F70BBEFE96BDDE66F451754B4CA5F48DA241F331AA396B8D1839A855C1769B1EA14BA53308B5E2723724E090E02DB9

    def __init__(self, hash=sha_256):
        self.hash = hash

        self.base_point = (self.BASE_X, self.BASE_Y)

        self.len_n = self.CURVE.n.bit_length()

    def gen_private_key(self):
        return random.randint(1, self.CURVE.n-1)

    def gen_public_key(self, d):
        neg_p = self.CURVE.negate_point(self.base_point)
        return self.CURVE.multiple_points(neg_p, d)

    def sign(self, message, private_key):

        h = self.hash(message)

        r, s, randSignPoint = 0, 0, None
        while r == 0 or s == 0:
            x = 0
            while x == 0:
                k = random.randint(1, self.CURVE.n-1)
                x, y = self.CURVE.multiple_points(self.base_point, k)

            r = self.CURVE.FIELD.mul(h, x) & self.CURVE.n
            s = ((k + private_key * r) * (self.CURVE.FIELD.inversion(k, self.CURVE.n))) % self.CURVE.n

        return (r, s)

    def verify(self, message, signature, public_key):

        h = self.hash(message)

        r, s = signature
        assert 0 < r < self.CURVE.n
        assert 0 < s < self.CURVE.n
        mul_q = self.CURVE.multiple_points(public_key, r)
        mul_s = self.CURVE.multiple_points(self.base_point, s)

        x, y = self.CURVE.add_points(mul_s, mul_q)
        r2 = self.CURVE.FIELD.multiplication(h, x) & self.CURVE.n
        if r != r2:
            return False
        return True

if __name__ == '__main__':
    ECDSA()