import abc


class Listener(metaclass=abc.ABCMeta):
    """Abstract class to provide a common interface for listeners"""

    @abc.abstractmethod
    def process_soon(self, msg):
        pass

    @abc.abstractmethod
    def listen(self):
        pass
