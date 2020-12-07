import numpy as np

encode = lambda x: np.array([ord(c) for c in x], dtype=np.uint8)

decode = lambda x: bytes(x).decode("utf-8")
