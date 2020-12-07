from field import Field


class Curve:
    INF = (0, 0)
    FIELD = Field([431, 5, 3, 1, 0])

    def __init__(self, A, B, n):
        self.A, self.B, self.n = A, B, n

    def point_generation(self):
        while True:
            x = self.FIELD.get_random_value()
            x_3 = self.FIELD.power(x, 3)
            x_2 = self.FIELD.sqr(x)
            A_x_2 = self.FIELD.multiplication(self.A, x_2)
            x_3_plus_A_x_2 = self.FIELD.add(x_3, A_x_2)
            x_3_plus_A_x_2_plus_B = self.FIELD.add(x_3_plus_A_x_2, self.B)

            if x == 0:
                return 0, self.FIELD.power(x_3_plus_A_x_2_plus_B, 2 ** (self.FIELD.m - 1))
            elif x_3_plus_A_x_2_plus_B == 0:
                return x, 0
            else:
                x_inversion = self.FIELD.inversion(x)
                sqr_x_inversion = self.FIELD.sqr(x_inversion)
                v = self.FIELD.multiplication(x_3_plus_A_x_2_plus_B, sqr_x_inversion)
                if self.FIELD.trace(v) == 1:
                    continue
                else:
                    t = self.FIELD.half_trace(v)
                    return x, self.FIELD.multiplication(t, x)

    def add_points(self, point1, point2):
        if point1 == self.INF:
            return point2
        elif point2 == self.INF:
            return point1
        elif point1 == point2:
            return self.double_point(point1)
        elif point2 == self.negate_point(point1):
            return self.INF
        else:
            x1, y1 = point1
            x2, y2 = point2

            x1_plus_x2 = self.FIELD.add(x1, x2)
            y1_plus_y2 = self.FIELD.add(y1, y2)
            lamb = self.FIELD.division(y1_plus_y2, x1_plus_x2)
            lamb_2_plus_lamb = self.FIELD.add(self.FIELD.sqr(lamb), lamb)
            lamb_2_plus_lamb_plus_A = self.FIELD.add(lamb_2_plus_lamb, self.A)

            x3 = self.FIELD.add(lamb_2_plus_lamb_plus_A, x1_plus_x2)

            x1_plus_x3_lamd = self.FIELD.multiplication(lamb, self.FIELD.add(x1, x3))
            x3_plus_y1 = self.FIELD.add(x3, y1)

            y3 = self.FIELD.add(x1_plus_x3_lamd, x3_plus_y1)

            return x3, y3

    def double_point(self, point):
        x, y = point

        mu = self.FIELD.add(x, self.FIELD.division(y, x))
        mu_2 = self.FIELD.sqr(mu)
        mu_2_plus_mu = self.FIELD.add(mu_2, mu)

        x3 = self.FIELD.add(mu_2_plus_mu, self.A)

        x_2 = self.FIELD.sqr(x)

        mu_plus_1_x3 = self.FIELD.multiplication(self.FIELD.add(mu, 1), x3)

        y3 = self.FIELD.add(x_2, mu_plus_1_x3)
        return x3, y3

    def is_point_on_curve(self, point):
        if point == self.INF:
            return True
        x, y = point

        x_3 = self.FIELD.power(x, 3)
        x_2 = self.FIELD.sqr(x)
        A_x_2 = self.FIELD.multiplication(self.A, x_2)
        x_3_plus_A_x_2 = self.FIELD.add(x_3, A_x_2)
        x_3_plus_A_x_2_plus_B = self.FIELD.add(x_3_plus_A_x_2, self.B)

        y_2 = self.FIELD.sqr(y)
        xy = self.FIELD.multiplication(x, y)
        y_2_plus_xy = self.FIELD.add(y_2, xy)

        return y_2_plus_xy == x_3_plus_A_x_2_plus_B

    def negate_point(self, point):
        x, y = point
        return x, self.FIELD.add(x, y)

    def multiple_points(self, point, n):
        q = (0, 0)
        while n > 0:
            if n & 1 == 1:
                q = self.add_points(q, point)
            point = self.double_point(point)
            n = n >> 1
        return q

if __name__ == '__main__':
    curve = Curve(A=1,
                  B=0x03CE10490F6A708FC26DFE8C3D27C4F94E690134D5BFF988D8D28AAEAEDE975936C66BAC536B18AE2DC312CA493117DAA469C640CAF3,
                  n=0x3FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFBA3175458009A8C0A724F02F81AA8A1FCBAF80D90C7A95110504CF)

    p = curve.point_generation()
    print("Generated point P:", p)
    q = curve.point_generation()
    print("Generated point Q:", q)

    print("Is P on curve:", curve.is_point_on_curve(p))
    print("Is Q on curve:", curve.is_point_on_curve(q))

    neg_r = curve.add_points(p, q)
    print("Sum P+Q=-R :", neg_r)
    print("Is -R on curve:", curve.is_point_on_curve(neg_r))

    neg_p = curve.negate_point(p)
    neg_q = curve.negate_point(q)
    print("Calculate -P:", neg_p)
    print("Calculate -Q:", neg_q)

    print("Is -P on curve:", curve.is_point_on_curve(neg_p))
    print("Is -Q on curve:", curve.is_point_on_curve(neg_q))

    print("Sum (-P)+(-Q)+(-R):", curve.add_points(neg_r, curve.add_points(neg_p, neg_q)))

    double_p = curve.double_point(p)
    print("Calculate 2P:", double_p)
    print("Is 2P on curve:", curve.is_point_on_curve(double_p))
    print("Is 2P == P+P on curve:", double_p == curve.add_points(p, p))

    p_mult_11 = curve.multiple_points(p, 11)

    p_sum = curve.INF
    for i in range(11):
        p_sum = curve.add_points(p_sum, p)

    print("Is 11P == P+P+...+P+P on curve:", p_sum == p_mult_11)
