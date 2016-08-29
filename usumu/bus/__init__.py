import abc

class Bus(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def publish(self, msg):
        """Publishes message to bus"""
        pass

