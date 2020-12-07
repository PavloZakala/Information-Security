import time


def proof_of_work(header: bytearray, difficulty_bits, hash_function):
    target = 2 ** (256 - difficulty_bits)
    for nonce in range(2 ** 32):

        hash_result = hash_function(header + bytearray(str(nonce), 'utf-8'))

        num = int.from_bytes(hash_result, byteorder='big')
        if num < target:
            print("Success with nonce %d" % nonce)
            print("Hash is %s" % hash_result.hex())
            return (hash_result, nonce)

    print("Failed after {} {} tries".format(nonce, 2 ** 32))
    return nonce


if __name__ == '__main__':

    from sha_256 import sha_256
    from kupyna import kupyna


    def kupyna_256(message: bytearray):
        return kupyna(message, 256)


    HEADER = bytearray("-----> Box of text! <-----", 'utf-8')
    RANGE = range(7, 15)
    print("SHA-256")

    for i in RANGE:
        print("")
        print("Difficult", i)
        start_time = time.time()
        proof_of_work(HEADER, i, sha_256)
        end_time = time.time()
        print("Elapsed time: %.4f seconds" % (end_time - start_time))

    print("KUPYNA-256")
    for i in RANGE:
        print("")
        print("Difficult", i)
        start_time = time.time()
        proof_of_work(HEADER, i, kupyna_256)
        end_time = time.time()
        print("Elapsed time: %.4f seconds" % (end_time - start_time))
