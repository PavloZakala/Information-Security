from random import randint

def miller_rabin_test(n, k=1000):
    def decompose(n):
        s = 0
        while n % 2 == 0:
            s += 1
            n //= 2
        return s, n

    if n < 2:
        return False
    if n < 4:
        return True
    if n % 2 == 0:
        return False

    s, d = decompose(n - 1)
    for _ in range(k):
        a = randint(2, n - 1)
        x = pow(a, d, n)
        if x == 1:
            continue
        for _ in range(s):
            if x == n - 1:
                break
            x = x ** 2 % n
        else:
            return False
    return True


if __name__ == '__main__':
    from tqdm import tqdm

    prime_number = [4001, 4003, 4007, 4013, 4019, 4021, 4027, 4049, 4051, 4057, 4073, 4079, 4091, 4093, 4099, 4111,
                    4127, 4129, 4133, 4139, 4153, 4157, 4159, 4177, 4201, 4211, 4217, 4219, 4229, 4231, 4241, 4243,
                    4253, 4259, 4261, 4271, 4273, 4283, 4289, 4297, 4327, 4337, 4339, 4349, 4357, 4363, 4373, 4391,
                    4397, 4409, 4421, 4423, 4441, 4447, 4451, 4457, 4463, 4481, 4483, 4493, 4507, 4513, 4517, 4519,
                    4523, 4547, 4549, 4561, 4567, 4583, 4591, 4597, 4603, 4621, 4637, 4639, 4643, 4649, 4651, 4657,
                    4663, 4673, 4679, 4691, 4703, 4721, 4723, 4729, 4733, 4751, 4759, 4783, 4787, 4789, 4793, 4799,
                    4801, 4813, 4817, 4831, 4861, 4871, 4877, 4889, 4903, 4909, 4919, 4931, 4933, 4937, 4943, 4951,
                    4957, 4967, 4969, 4973, 4987, 4993, 4999]

    for n in tqdm(range(4000, 5000)):
        if miller_rabin_test(n):
            if n not in prime_number:
                raise ModuleNotFoundError()

    print(True)
