from abc import abstractmethod
import numpy as np

class BaseMode:

    def __init__(self, cipher, n=16):

        self._cipher = cipher
        self._n = n

    @abstractmethod
    def encrypt(self, plaintext: np.array):
        pass

    @abstractmethod
    def decrypt(self, ciphertext: np.array):
        pass