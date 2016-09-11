from abc import ABCMeta, abstractmethod


class Bus(metaclass=ABCMeta):
    @abstractmethod
    def publish(self, msg):
        """Publishes message to bus"""
        pass


class Default(Bus):  # default bus driver is a dummy driver, it does not do anything
    def publish(self, msg):
        pass
