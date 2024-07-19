from abc import ABC, abstractmethod


class DataDecrypter(ABC):


    @abstractmethod
    def _DecryptWithKey(self, data):
        pass

