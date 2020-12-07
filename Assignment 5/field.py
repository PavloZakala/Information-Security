import random

class Field(object):

    def __init__(self, degrees):
        self.m = 431
        self.__BINARY_F = 0
        for d in degrees:
            self.__BINARY_F = self.__BINARY_F + 2 ** d

        self.__MAX_V = 2 ** self.m - 1

    def get_random_value(self):
        return random.randint(0, self.__MAX_V)

    def add(self, v1, v2):
        return v1 ^ v2

    def multiplication(self, v1, v2):
        res = 0
        while v1 and v2:
            if v2 & 1 == 1:
                res ^= v1
            v2 >>= 1
            b = v1 >> (self.m - 1)
            v1 = (v1 << 1) & self.__MAX_V
            if b == 1:
                v1 ^= self.__MAX_V & self.__BINARY_F
        return res

    def power(self, v, n):
        res = 1
        while n > 0:
            if n & 1 == 1:
                res = self.multiplication(v, res)
            v = self.multiplication(v, v)
            n = n >> 1
        return res

    def sqr(self, v):
        return self.multiplication(v, v)

    def inversion(self, point):
        return self.power(point, (1 << self.m) - 2)

    def division(self, v1, v2):
        v2_inversion = self.inversion(v2)
        return self.multiplication(v1, v2_inversion)

    def trace(self, a):
        res = a
        for i in range(self.m - 1):
            res = self.add(self.sqr(res), a)
        return res

    def half_trace(self, a):
        res = a
        for i in range((self.m - 1) // 2):
            res = self.add(self.sqr(self.sqr(res)), a)
        return res

    def solve_quadratic_eq(self, u, w):
        if u == 0:
            z = self.power(w, 2 ** (self.m - 1))
            return z, 1
        if w == 0:
            return 0, 2
        u_inversion = self.inversion(u)
        sqr_u_inversion = self.sqr(u_inversion)
        v = self.multiplication(w, sqr_u_inversion)
        if self.trace(v) == 1:
            return 0, 0
        t = self.half_trace(v)
        return self.multiplication(t, u), 2
