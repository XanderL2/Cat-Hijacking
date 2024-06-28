from abc import ABC, abstractmethod


class DataDecrypter(ABC):


    @abstractmethod
    def __DecryptWithKey(self, data):
        pass

